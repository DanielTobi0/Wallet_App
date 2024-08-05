from urls import get_paths


class App:
    def __init__(self):
        self.app_active = None

        self.paths = get_paths()

        self.actions = {
            '1': self.signup,
            '2': self.signin,
            '12': self.exit_app
        }

    def signup(self):
        self.paths['signup']()

    def signin(self):
        path_dict = get_paths()
        success, name, wallet_id_ = self.paths['signin']()
        path_dict['username'] = name
        path_dict['wallet'] = wallet_id_

        signin_app_active = True
        state = {'signin_app_active': signin_app_active}
        while success and state['signin_app_active']:
            path_dict['signin_flow'](path_dict['username'], state, path_dict['wallet']) # signin_flow(username, state, wallet_id)

    def exit_app(self):
        print('\nGoodbye!!')
        self.app_active = False

    def invalid_selection(self):
        print('error 404')

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
            action = self.actions.get(user_input, self.invalid_selection)
            action()


app = App()
app.run()
