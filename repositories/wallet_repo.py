import psycopg2
import psycopg2.extras
from helpers.helpers import get_connection
from models.wallet import Wallet
from repositories.user_repo import UserFileRepository


class WalletFileRepository:

    @classmethod
    def get_wallet_id_by_username(cls, username):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute(
                '''SELECT wallet_id FROM wallet_db WHERE username = %s''',
                (username,)
            )
            return cur.fetchone()[0]

        finally:
            cur.close()
            conn.close()

    @classmethod
    def get_username_by_wallet_id(cls, wallet_id):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute(
                'SELECT username FROM wallet_db WHERE wallet_id = %s',
                (wallet_id,)
            )
            result = cur.fetchone()
            conn.commit()
            return result['username']

        except Exception as e:
            print(f'error: {e}')

        finally:
            cur.close()
            conn.close()

    @classmethod
    def get_balance(cls, wallet_id):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(
            'SELECT balance FROM wallet_db WHERE wallet_id = %s',
            (wallet_id,)
        )
        return float(cur.fetchone()[0])

    @classmethod
    def update_balance(cls, amount, wallet_id):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(
            'UPDATE wallet_db SET balance = %s WHERE wallet_id = %s',
            (amount, wallet_id,)
        )
        conn.commit()

    @classmethod
    def deposit(cls, wallet_id_, amount: float):
        try:
            current_balance = cls.get_balance(wallet_id_)
            amount = float(amount)
            new_balance = current_balance + amount
            cls.update_balance(amount=new_balance, wallet_id=wallet_id_)
            updated_price = cls.get_balance(wallet_id=wallet_id_)  # current price after deposit

            print(f'{amount} successfully deposited')
            print(f'Current balance: {updated_price}\n\n')

            return cls.get_username_by_wallet_id(wallet_id_)

        except Exception as e:
            print(f'error: {e}')

    @classmethod
    def withdrawal(cls, wallet_id_: str, amount: float):
        if not isinstance(amount, (float, int)):
            print('amount should be numerical not text')
            return
        elif amount < 0:
            print('Ogbon sodiki!')
            return
        try:
            # get balance
            current_price = cls.get_balance(wallet_id=wallet_id_)
            if not current_price:
                print(f'wallet id {wallet_id_} not found.')
                return

            if current_price < amount:
                print(f'\n******Your account balance is too low. {current_price}******\n')
                return
            else:
                new_balance = current_price - float(amount)
                cls.update_balance(new_balance, wallet_id_)
                print(f'{amount} successfully withdraw')
                print(f'Current balance: {new_balance}\n\n')

                return cls.get_username_by_wallet_id(wallet_id_)

        except Exception as e:
            print(f'An error occurred: {e}')

    @classmethod
    def send_money(cls, wallet_id_: str, amount: float, receiver: str):
        # check is amount is not text or less than 0
        if not isinstance(amount, (float, int)):
            print('amount should be numerical not text')
            return
        elif float(amount) < 0:
            print('Ogbon sodiki!')
            print('Amount should be greater than zero!')
            return

        # is this okay :) ?
        # check if receiver is valid
        result = UserFileRepository.check_user_existence_by_username(receiver)
        if not isinstance(result, bool):
            print('User not found')
            return

        # use the sender wallet_id to get username, for comparison to receiver username
        sender_username = cls.get_username_by_wallet_id(wallet_id_)
        if sender_username == receiver:
            print('You can not send money to yourself')
            return

        try:
            # get sender balance
            sender_balance = cls.get_balance(wallet_id_)
            if sender_balance < amount:
                print(
                    f'\n****** Your account balance is too low to make this transfer.******\n****** Current balance: {sender_balance} ******\n')
                return

            # debit sender
            amount = float(amount)
            new_balance = sender_balance - amount
            cls.update_balance(new_balance, wallet_id_)

            # get receiver's wallet_id and balance
            receiver_wallet_id = cls.get_wallet_id_by_username(receiver)
            receiver_balance = cls.get_balance(receiver_wallet_id)

            # credit receiver
            update_receiver_balance = receiver_balance + amount
            cls.update_balance(update_receiver_balance, receiver_wallet_id)

            # get username of sender by wallet_id
            result = cls.get_username_by_wallet_id(wallet_id_)

            print(f'You sent {amount} to {receiver}\nCurrent balance: {cls.get_balance(wallet_id_)}\n')
            print('Transaction completed successfully')
            return result

        except Exception as e:
            print(f'an error occurred: {e}')

    @classmethod
    def check_balance(cls, wallet_id_):
        balance = cls.get_balance(wallet_id_)
        print(f'Balance: {balance}')

    @classmethod
    def create_wallet(cls, wallet_db: Wallet):
        cur = None
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            create_script = '''CREATE TABLE IF NOT EXISTS wallet_db (
                                                    walled_id VARCHAR(255),
                                                    balance float,
                                                    username VARCHAR(255),
                                                    created_at VARCHAR(255),
                                                    updated_at VARCHAR(255)
                                                    )'''
            cur.execute(create_script)

            insert_script = (
                'INSERT INTO wallet_db (wallet_id, balance, username, created_at, updated_at) '
                'VALUES (%s, %s, %s, %s, %s)'
            )
            values = (
                wallet_db.wallet_id,
                wallet_db.balance,
                wallet_db.username,
                wallet_db.created_at,
                wallet_db.updated_at
            )

            cur.execute(insert_script, values)
            conn.commit()
            print(f'\n********************* {wallet_db.username} profile created *********************\n')

        except Exception as error:
            raise error
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def profile(cls, wallet_id_):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute(
                "SELECT * FROM wallet_db WHERE wallet_id = %s LIMIT 1",
                (wallet_id_,)
            )
            user_row = cur.fetchone()
            if user_row:
                for key, value in user_row.items():
                    print(f'{key}: {value}')
            else:
                print(f'User not found\n\n')
        finally:
            print('\n\n')
            cur.close()
            conn.close()
