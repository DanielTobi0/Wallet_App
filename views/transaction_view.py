from controllers.transaction_controller import TransactionFileRepository


class TransactionView:

    @staticmethod
    def handle_get_transaction(username):
        return TransactionFileRepository.get_user_transactions_id_by_username(username)

    @staticmethod
    def get_single_transaction_id_by_username_():
        transaction_id = input('Enter transaction id: ')
        TransactionFileRepository.get_single_transaction_by_transaction_id(transaction_id)
