from datetime import datetime

from helpers import load_data, write_to_db
from models import User, Wallet, Transaction
from utils import users_db_path, transactions_db_path, wallets_db_path


class UserFileRepository:
    users = load_data(users_db_path, User)
    wallets = load_data(wallets_db_path, Wallet)

    @classmethod
    def create(cls, name, email, phone, username, password, wallet_id, created_at):
        if any(user.username == username for user in cls.users):
            print(f'Username "{username}" is already taken. Please choose a different username.')
            return

        # User info save to db
        new_user = User(name, email, phone, username, password, created_at)
        UserFileRepository.users.append(new_user)
        write_to_db(users_db_path, UserFileRepository.users)

        # Wallet info save to db
        balance = 0.0
        new_wallet = Wallet(wallet_id, balance, username)
        WalletFileRepository.wallets.append(new_wallet)
        write_to_db(wallets_db_path, WalletFileRepository.wallets)

        print(f'\n*********************{username} profile created*********************\n')
        return new_user.to_dict()

    @classmethod
    def delete_user_by_username(cls, username):
        """
        This function deletes a user from user and wallet database, using username
        """
        cls.users = [user for user in cls.users if user.username != username]
        cls.wallets = [wallet for wallet in cls.wallets if wallet.username != username]
        write_to_db(users_db_path, cls.users)
        write_to_db(wallets_db_path, cls.wallets)
        print(f'\n*********************{username} profile deleted from db.*********************\n')

    @classmethod
    def get_user_by_username(cls, username):
        for user_data in cls.users:
            if user_data.username == username:
                return user_data.to_dict()
        return None

    @classmethod
    def authenticate_login(cls, username: str, password: str):
        for idx, user_data in enumerate(load_data(users_db_path, User)):
            if user_data.username == username and user_data.password == password:
                print(f'login successful\n')
                return True, user_data.username, cls.wallets[idx - 1].wallet_id
        print('\n*********************Login failed*********************\n')
        return False, None, None

    @classmethod
    def profile(cls, username):
        users = load_data(users_db_path, User)
        wallets = load_data(wallets_db_path, Wallet)
        for idx, user in enumerate(users):
            if user.username == username:
                print(users[idx].to_dict())
                print(wallets[idx].to_dict())


class WalletFileRepository:
    wallets = load_data(wallets_db_path, Wallet)

    @classmethod
    def create(cls):
        wallet_id = str(len(cls.wallets))
        balance = int(0)
        username = str(None)
        return Wallet(wallet_id, balance, username)

    @classmethod
    def get_user_by_username(cls, username):
        for user_name_ in cls.wallets:
            if user_name_.username == username:
                return user_name_.to_dict()
        return None

    @classmethod
    def deposit(cls, username, amount):
        try:
            amount = float(amount)
        except ValueError:
            print('Enter amount in numbers')
            return

        for idx, user_name in enumerate(cls.wallets):
            if user_name.username == username:
                cls.wallets[idx].balance += amount
                TransactionFileRepository.create(username, amount, 'deposit', '')
        write_to_db(wallets_db_path, cls.wallets)
        print(f'Successfully deposited {amount} into your account.\n')

    @classmethod
    def withdrawal(cls, username, amount):
        try:
            amount = float(amount)
        except ValueError:
            print('enter amount in numbers')
            return

        for idx, user in enumerate(cls.wallets):
            if user.username == username:
                if user.balance < amount:
                    print(f'\n******Your account balance is too low. {user.balance}******\n')
                    return
                cls.wallets[idx].balance -= amount
                write_to_db(wallets_db_path, cls.wallets)
                TransactionFileRepository.create(username, amount, 'withdrawal', '')
                print(f'Your balance is #{cls.wallets[idx].balance}\n\n')
                return

    @classmethod
    def send_money(cls, source, amount, recipient):
        try:
            amount = float(amount)
        except ValueError:
            print('enter amount in numbers')
            return

        if source == recipient:
            print('Cannot send money to yourself.')
            return

        source_wallet = None
        recipient_wallet = None

        for wallet in cls.wallets:
            if wallet.username == source:
                source_wallet = wallet
            if wallet.username == recipient:
                recipient_wallet = wallet

        if source_wallet is None:
            print('Source username not found.')
            return
        if recipient_wallet is None:
            print('Recipient username not found.')
            return

        if source_wallet.balance < amount:
            print(f'Insufficient funds.')
            return

        source_wallet.balance -= amount
        recipient_wallet.balance += amount

        for idx, wallet in enumerate(cls.wallets):
            if wallet.username == source:
                cls.wallets[idx] = source_wallet
            if wallet.username == recipient:
                cls.wallets[idx] = recipient_wallet

        write_to_db(wallets_db_path, cls.wallets)
        TransactionFileRepository.create(source, amount, 'debit', recipient)
        print(f'#{amount} sent from {source} to {recipient}.')
        # print(f'{source} new balance: {source_wallet.balance}')
        # print(f'{recipient} new balance: {recipient_wallet.balance}')

    @classmethod
    def check_balance(cls, username):
        for idx, wallet in enumerate(cls.wallets):
            if wallet.username == username:
                print(f'\n*********************Balance: {cls.wallets[idx].balance}*********************\n')

    @staticmethod
    def profile(username):
        wallets = load_data(wallets_db_path, Wallet)
        for idx, user in enumerate(wallets):
            if user.username == username:
                print(wallets[idx].to_dict())


class TransactionFileRepository:
    transactions = load_data(transactions_db_path, Transaction)

    @classmethod
    def create(cls, sender, amount, transaction_type=None, receiver=''):
        created_at = str(datetime.now().isoformat())
        transaction_id = sender + '-' + receiver + created_at
        transaction = Transaction(transaction_id, created_at, sender, receiver, amount, transaction_type)
        cls.transactions.append(transaction)
        write_to_db(transactions_db_path, cls.transactions)

    @classmethod
    def get_user_transaction_id_by_username(cls, username):
        for transaction in cls.transactions:
            if transaction.sender == username:
                print(transaction.to_dict())

    @classmethod
    def get_single_transaction_id_by_username(cls, transaction_id):
        for transaction in cls.transactions:
            if transaction.transaction_id == transaction_id:
                print(transaction.to_dict())
                return
        print('\n*********************Transaction not found!*********************\n')
