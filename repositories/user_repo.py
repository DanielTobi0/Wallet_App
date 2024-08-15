import hashlib

import psycopg2
import psycopg2.extras
from models.user import User
from helpers.helpers import get_connection


class UserFileRepository:
    @classmethod
    def hash_password(cls, password):
        h = hashlib.new("SHA256")
        h.update(password.encode())
        return h.hexdigest()

    @classmethod
    def check_user_existence_by_username(cls, username):
        """
        :param username: unique id of each user
        :return: True if user exists in the db
        """
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('''SELECT EXISTS (SELECT username FROM user_db WHERE username = %s)''', (username,))
        result = cur.fetchone()[0]
        if result:
            return result

    @classmethod
    def create(cls, user: User):
        conn = None
        cur = None
        user.password = cls.hash_password(user.username)

        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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

        except Exception as error:
            raise error
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def authenticate_login(cls, username: str, password: str):
        # current user entered password, then compare
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # authenticate user Username and Password
        password = cls.hash_password(password) # get hash equivalent
        cur.execute('''SELECT EXISTS(SELECT * FROM user_db WHERE username = %s and password = %s)''',
                    (username, password))
        return cur.fetchall()[0][0]

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
