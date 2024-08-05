from datetime import datetime
import random

from models.user import User
from models.wallet import Wallet
from views.transaction_view import TransactionView
from views.wallet_view import WalletView
from controllers.user_controller import UserFileRepository
from controllers.wallet_controller import WalletFileRepository


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
        balance = 0.0

        user = User(name, email, phone, username, password, created_at)
        if UserFileRepository.create(user):
            wallet = Wallet(wallet_id, balance, username)
            WalletFileRepository.create_wallet(wallet)

    @staticmethod
    def signin():
        username = input('Enter username: ')
        password = input('Enter password: ')
        success, name, wallet_id_ = UserFileRepository.authenticate_login(username, password)
        if success:
            print(f'\n********************* Login successful *********************\n')
        return success, name, wallet_id_

    @staticmethod
    def signin_flow(username, state, wallet_id):
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
                WalletView.deposit_(wallet_id)
            elif user_input == '2':
                WalletView.withdraw_(wallet_id)
            elif user_input == '3':
                WalletView.send_money_(wallet_id)
            elif user_input == '4':
                WalletView.check_balance_(wallet_id)
            elif user_input == '5':
                TransactionView.handle_get_transaction(username)
            elif user_input == '6':
                WalletView.profile_(wallet_id)
            elif user_input == '7':
                UserView.profile_(username)
            elif user_input == '8':
                TransactionView.get_single_transaction_id_by_username_()
            elif user_input == '9':
                state['signin_app_active'] = False
            else:
                print("\ninvalid input\n")

    @classmethod
    def profile_(cls, username):
        UserFileRepository.profile(username)
