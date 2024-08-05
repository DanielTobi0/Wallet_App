from os import environ

# Database config
DATABASE_HOST = environ.get('hostname')
DATABASE_USERNAME = environ.get('username_db')
DATABASE_PASSWORD = environ.get('pwd')
DATABASE_PORT = environ.get('port_id')
DATABASE_NAME = environ.get('database')
