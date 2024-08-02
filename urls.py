from views import UserView, WalletView, TransactionView


def get_paths():
    return {
        "signup": UserView.signup,
        "wallet": WalletView.wallet,
        "signin": UserView.signin,
        "signin_flow": UserView.signin_flow,
        "deposit": WalletView.deposit_,
        "withdraw": WalletView.withdraw_,
        "balance": WalletView.check_balance_,
        "profile": UserView.profile,
        "wallet_profile": WalletView.profile_,
        "transaction": TransactionView.handle_get_transaction,
        "single_transaction": TransactionView.get_single_transaction_id_by_username_,
    }
