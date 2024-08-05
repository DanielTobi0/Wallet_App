import psycopg2
import psycopg2.extras
from helpers.helpers import get_connection
from models.wallet import Wallet


class WalletFileRepository:

    @classmethod
    def deposit(cls, wallet_id_, amount: float):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('SELECT balance FROM wallet_db WHERE wallet_id = %s', (wallet_id_,))
            current_price = cur.fetchone()[0]

            amount = float(amount)
            cur.execute('UPDATE wallet_db SET balance = %s WHERE wallet_id = %s', (amount + current_price, wallet_id_,))
            conn.commit()

            cur.execute('SELECT balance FROM wallet_db WHERE wallet_id = %s', (wallet_id_,))
            updated_price = cur.fetchone()[0]

            print(f'{amount} successfully deposited')
            print(f'Current balance: {updated_price}\n\n')

            # get username of wallet_id
            cur.execute('SELECT username FROM wallet_db WHERE wallet_id = %s', (wallet_id_,))
            result = cur.fetchone()
            conn.commit()
            return result['username']

        except Exception as e:
            print(f'error: {e}')

        finally:
            cur.close()
            conn.close()

    @classmethod
    def withdrawal(cls, wallet_id_: str, amount: float):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if not isinstance(amount, (float, int)):
            print('amount should be numerical not text')
            return
        elif amount < 0:
            print('Ogbon sodiki!')
            return
        try:
            cur.execute('SELECT balance FROM wallet_db WHERE wallet_id = %s', (wallet_id_,))
            result = cur.fetchone()
            if not result:
                print(f'wallet id {wallet_id_} not found.')
                return

            current_price = result['balance']

            if current_price < amount:
                print(f'\n******Your account balance is too low. {current_price}******\n')
                return
            else:
                new_balance = current_price - float(amount)
                cur.execute('UPDATE wallet_db SET balance = %s WHERE wallet_id = %s', (new_balance, wallet_id_,))

                print(f'{amount} successfully withdraw')
                print(f'Current balance: {new_balance}\n\n')

                # get username of wallet_id
                cur.execute('SELECT username FROM wallet_db WHERE wallet_id = %s', (wallet_id_,))
                result = cur.fetchone()
                conn.commit()
                return result['username']

        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            cur.close()
            conn.close()

    @classmethod
    def send_money(cls, wallet_id_: str, amount: float, receiver: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # check is amount is not text or less than 0
        if not isinstance(amount, (float, int)):
            print('amount should be numerical not text')
            return
        elif float(amount) < 0:
            print('Ogbon sodiki!')
            print('Amount should be greater than zero!')
            return

        # check if receiver exist in the database
        cur.execute('select exists (select wallet_id from wallet_db where username = %s)', (receiver,))
        result = cur.fetchone()[0]
        if not result:
            print('User not found')
            return

        # use the sender wallet_id to get username, for comparison
        cur.execute('select username from wallet_db where wallet_id = %s', (wallet_id_,))
        username = cur.fetchone()[0]

        if username == receiver:
            print('You can not send money to yourself')
            return

        try:
            # get sender balance
            cur.execute('SELECT balance FROM wallet_db WHERE username = %s', (username,))
            sender_balance = cur.fetchone()[0]

            if sender_balance < amount:
                print(
                    f'\n****** Your account balance is too low to make this transfer.******\n****** Current balance: {sender_balance} ******\n')
                return

            # debit sender
            amount = float(amount)
            new_balance = sender_balance - amount
            cur.execute('UPDATE wallet_db SET balance = %s WHERE username = %s', (new_balance, username))
            conn.commit()

            # get receiver's balance
            cur.execute('SELECT balance FROM wallet_db WHERE username = %s', (receiver,))
            result = cur.fetchone()
            receiver_balance = result['balance']

            # credit receiver
            cur.execute('UPDATE wallet_db SET balance = %s WHERE username = %s',
                        (receiver_balance + amount, receiver,))

            # get username of wallet_id
            cur.execute('SELECT username FROM wallet_db WHERE wallet_id = %s', (wallet_id_,))
            result = cur.fetchone()
            conn.commit()

            print(f'You sent {amount} to {receiver}\n\n')
            # print('Transaction completed successfully')
            return result['username']

        except Exception as e:
            conn.rollback()
            print(f'an error occurred: {e}')

        finally:
            cur.close()
            conn.close()

    @classmethod
    def check_balance(cls, wallet_id_):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = "SELECT * FROM wallet_db WHERE wallet_id = %s"
            cur.execute(query, (wallet_id_,))
            user_row = cur.fetchone()
            if user_row:
                for key, value in user_row.items():
                    if key == 'balance':
                        print(f'{key}: {value}\n\n')
        finally:
            cur.close()
            conn.close()

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
                'INSERT INTO wallet_db (wallet_id, balance, username, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)')
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
            cur.execute("SELECT * FROM wallet_db WHERE wallet_id = %s", (wallet_id_,))
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
