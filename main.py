from utils import users_db_path, transactions_db_path, wallets_db_path
from urls import get_path


class App:
    def __init__(self):
        self.app_active = None

        self.user = {}
        self.wallet = None
        self.transaction = None

        self.users = []
        self.wallets = []
        self.transactions = []

        self.user_db_path = users_db_path
        self.wallet_db_path = wallets_db_path
        self.transactions_db_path = transactions_db_path

        self.paths = get_path()

    def run(self):
        self.app_active = True

        print("Welcome to your HB wallet...")
        print("please wait while we setup your app")

        while self.app_active:
            print("\nEnter the corresponding numbers to perform an action.")
            user_input = str(input("1. Create Account\n"
                                   "2. Sign-in to your Account\n"
                                   "3. Deposit Money \n"
                                   "4. Withdraw Money \n"
                                   "5. Send Money \n"
                                   "6. Check Balance \n"
                                   "7. My Transactions \n"
                                   "8. My wallet\n"
                                   "9. My Profile\n"
                                   "10. View single transaction\n"
                                   "11. Sign out \n"
                                   "12. Exit App \n"
                                   ))
            if user_input == '1':
                self.paths['signup']()

            elif user_input == '2':
                path_dict = get_path()
                success, name, wallet_id_ = self.paths['signin']()
                path_dict['username'] = name
                path_dict['wallet'] = wallet_id_

                signin_app_active = True
                state = {'signin_app_active': signin_app_active}
                while success and state['signin_app_active']:
                    path_dict['signin_flow'](path_dict['username'], state)

            elif user_input in ['3', '4', '5', '6', '7', '8', '9', '10', '11']:
                print('You need to login first')

            elif user_input == '12':
                print('\nGoodbye!!')
                self.app_active = False

            else:
                print('Invalid selection')


app = App()
app.run()
