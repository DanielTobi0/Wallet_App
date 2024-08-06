import psycopg2
import psycopg2.extras
from helpers.helpers import get_connection
from models.transaction import Transaction


class TransactionFileRepository:

    @classmethod
    def get_user_transactions_id_by_username(cls, username):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute('SELECT * from transaction_db WHERE sender = %s', (str(username),))
            for record in cur.fetchall():
                print(f'{record}')
            print('\n\n')
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f'an error occurred: {e}')
        finally:
            cur.close()
            conn.close()

    @classmethod
    def get_single_transaction_by_transaction_id(cls, transaction_id):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute('SELECT * from transaction_db WHERE transaction_id = %s', (transaction_id,))
            result = cur.fetchone()
            if result is None:
                print('Transaction id not found')
            else:
                print(f'{result}\n\n')
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f'error encountered: {e}')
        finally:
            cur.close()
            conn.close()

    @classmethod
    def insert_transaction(cls, transaction_db: Transaction):

        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            create_script = '''CREATE TABLE IF NOT EXISTS transaction_db (
                                                    transaction_id VARCHAR(255),
                                                    created_at VARCHAR(255),
                                                    sender VARCHAR(255),
                                                    receiver VARCHAR(255),
                                                    amount float,
                                                    transaction_type VARCHAR(255) 
                                                    )'''
            cur.execute(create_script)

            insert_script = (
                'INSERT INTO transaction_db (transaction_id, created_at, sender, receiver, amount, transaction_type) '
                'VALUES (%s, %s, %s, %s, %s, %s)')
            values = (
                transaction_db.transaction_id,
                transaction_db.created_at,
                transaction_db.sender,
                transaction_db.receiver,
                transaction_db.amount,
                transaction_db.transaction_type
            )

            cur.execute(insert_script, values)
            conn.commit()

        except Exception as error:
            raise error
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
