from repositories import UserFileRepository, WalletFileRepository, TransactionFileRepository
from helpers import load_data
from models import Wallet, User
from utils import users_db_path, wallets_db_path


class UserView:

    @staticmethod
    def signup():
        UserFileRepository.create()
        WalletFileRepository.create()

    @staticmethod
    def signin():
        username = input('Enter username: ')
        password = input('Enter password: ')
        success, name, wallet_id_ = UserFileRepository.authenticate_login(username, password)
        return success, name, wallet_id_

    @staticmethod
    def signin_flow(username, state):
        while state['signin_app_active']:
            user_input = str(input("1. Deposit Money \n"
                                   "2. Withdraw Money \n"
                                   "3. Send Money \n"
                                   "4. Check Balance \n"
                                   "5. My Transactions \n"
                                   "6. My wallet\n"
                                   "7. My Profile\n"
                                   "8. View single transaction\n"
                                   "9. Sign out \n"
                                   ))
            if user_input == '1':
                WalletView.deposit_(username)
            elif user_input == '2':
                WalletView.withdraw_(username)
            elif user_input == '3':
                WalletFileRepository.send_money(source=username)
            elif user_input == '4':
                WalletFileRepository.check_balance(username)
            elif user_input == '5':
                TransactionView.handle_get_transaction(username)
            elif user_input == '6':
                WalletView.profile(username)
            elif user_input == '7':
                UserView.profile(username)
            elif user_input == '8':
                TransactionView.handle_single_transaction()
            elif user_input == '9':
                state['signin_app_active'] = False
            else:
                print("\ninvalid input\n")

    @staticmethod
    def authenticate_login_(username, password):
        return UserFileRepository.authenticate_login(username=username, password=password)

    @classmethod
    def profile(cls, username):
        users = load_data(users_db_path, User)
        wallets = load_data(wallets_db_path, Wallet)
        for idx, user in enumerate(users):
            if user.username == username:
                print(users[idx].to_dict())
                print(wallets[idx].to_dict())


class WalletView:

    @staticmethod
    def deposit_(username):
        result = WalletFileRepository.deposit(username=username)
        if result:
            return 'Deposit successful'
        else:
            return 'User not found'

    @staticmethod
    def withdraw_(username):
        WalletFileRepository.withdrawal(username)

    @staticmethod
    def check_balance(username):
        for user in load_data(wallets_db_path, Wallet):
            if user.username == username:
                return user.balance

    @staticmethod
    def profile(username):
        wallets = load_data(wallets_db_path, Wallet)
        for idx, user in enumerate(wallets):
            if user.username == username:
                print(wallets[idx].to_dict())


class TransactionView:

    @staticmethod
    def handle_get_transaction(username):
        return TransactionFileRepository.get_user_transaction_id_by_username(username)

    @staticmethod
    def handle_single_transaction():
        return TransactionFileRepository.get_single_transaction_id_by_username()