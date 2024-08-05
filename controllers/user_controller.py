import psycopg2
import psycopg2.extras
from models.user import User
from helpers.helpers import get_connection


class UserFileRepository:

    @classmethod
    def create(cls, user: User):
        conn = None
        cur = None

        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute('''SELECT EXISTS (SELECT username FROM user_db WHERE username = %s)''', (user.username,))
            result = cur.fetchone()[0]  # [bool] -> indexed 0

            if result:
                print('Username already not available')
                return False
            else:
                create_script = ''' CREATE TABLE IF NOT EXISTS user_db (
                                            name VARCHAR(40),
                                            email VARCHAR(40),
                                            phone VARCHAR(15),
                                            username VARCHAR(15),
                                            password VARCHAR(255),
                                            created_at VARCHAR(26)

                                    )'''
                cur.execute(create_script)

                insert_script = ('INSERT INTO user_db (name, email, phone, username, password, created_at) VALUES '
                                 '(%s, %s, %s, %s, %s, %s)')
                insert_values = (
                    user.name,
                    user.email,
                    user.phone,
                    user.username,
                    user.password,
                    user.created_at
                )
                cur.execute(insert_script, insert_values)
                conn.commit()
            return True

        except Exception as error:
            raise error
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def authenticate_login(cls, username: str, password: str):

        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('''SELECT EXISTS(SELECT * FROM user_db WHERE username = %s and password = %s)''',
                    (username, password))
        result = cur.fetchall()[0][0]

        if result:
            # grab user wallet_id from wallet_db
            cur.execute('''SELECT wallet_id FROM wallet_db WHERE username = %s''', (username,))
            wallet_id = cur.fetchone()[0]
            return True, username, wallet_id
        else:
            print('\n*********************Login failed*********************\n')
            return False, None, None

    @classmethod
    def profile(cls, username):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute('SELECT * FROM user_db WHERE username = %s', (username,))
            user_row = cur.fetchone()
            if user_row:
                for key, value in user_row.items():
                    print(f'{key}: {value}')
            else:
                print(f'User not found')
        finally:
            print('\n\n')
            cur.close()
            conn.close()
