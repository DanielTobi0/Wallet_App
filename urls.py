from views import UserView, WalletView, TransactionView


def get_path():
    return {
        "signup": UserView.signup,
        "wallet": str,
        "signin": UserView.signin,
        "signin_flow": UserView.signin_flow,
        "deposit": WalletView.deposit_,
        "withdraw": WalletView.withdraw_,
        "balance": WalletView.check_balance,
        "profile": UserView.profile,
        "delete": None,
        "wallet_profile": WalletView.profile,
        "transaction": TransactionView.handle_get_transaction,
        "single_transaction": TransactionView.handle_single_transaction,
    }