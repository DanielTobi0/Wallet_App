from datetime import datetime
import random

from repositories import UserFileRepository, WalletFileRepository, TransactionFileRepository


class UserView:

    @staticmethod
    def signup():
        name = input('Enter your name: ')
        email = input('Enter your email: ')
        phone = str(input('Enter your phone number: '))
        username = input('Enter your username: ')
        password = str(input('Enter your password: '))
        wallet_id = str(random.randint(1, 1000000))
        created_at = str(datetime.now().isoformat())

        UserFileRepository.create(name, email, phone, username, password, wallet_id, created_at)
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
                WalletView.send_money_(source=username)
            elif user_input == '4':
                WalletView.check_balance_(username)
            elif user_input == '5':
                TransactionView.handle_get_transaction(username)
            elif user_input == '6':
                WalletView.profile_(username)
            elif user_input == '7':
                UserView.profile(username)
            elif user_input == '8':
                TransactionView.get_single_transaction_id_by_username_()
            elif user_input == '9':
                state['signin_app_active'] = False
            else:
                print("\ninvalid input\n")

    @staticmethod
    def authenticate_login_(username, password):
        return UserFileRepository.authenticate_login(username=username, password=password)

    @classmethod
    def profile(cls, username):
        WalletFileRepository.profile(username)


class WalletView:
    wallet = str

    @staticmethod
    def deposit_(username):
        amount = input('Enter amount to deposit: ')
        result = WalletFileRepository.deposit(username=username, amount=amount)
        if result:
            return 'Deposit successful'
        else:
            return 'User not found'

    @staticmethod
    def withdraw_(username):
        amount = input('Enter amount to withdraw: ')
        WalletFileRepository.withdrawal(username, amount)

    @staticmethod
    def send_money_(source):
        recipient = str(input('Enter recipient username: '))
        amount = input('Enter amount to send: ')
        WalletFileRepository.send_money(source, amount, recipient)

    @staticmethod
    def check_balance_(username):
        WalletFileRepository.check_balance(username)

    @staticmethod
    def profile_(username):
        WalletFileRepository.profile(username)


class TransactionView:

    @staticmethod
    def handle_get_transaction(username):
        return TransactionFileRepository.get_user_transaction_id_by_username(username)

    @staticmethod
    def get_single_transaction_id_by_username_():
        transaction_id = input('Enter transaction id: ')
        TransactionFileRepository.get_single_transaction_id_by_username(transaction_id)
