from datetime import datetime

from models.transaction import Transaction
from repositories.wallet_repo import WalletFileRepository
from repositories.transaction_repo import TransactionFileRepository


class WalletView:
    wallet = str

    @staticmethod
    def deposit_(wallet_id__):
        amount = input('Enter amount to deposit: ')
        try:
            amount = float(amount)
            username = WalletFileRepository.deposit(wallet_id_=wallet_id__, amount=amount)

            created_at = datetime.now().isoformat()
            transaction_id = str(created_at) + '-' + str(amount)
            receiver = ''
            sender = username
            transaction_type = 'credit'
            transaction = Transaction(transaction_id, created_at, sender, receiver, amount, transaction_type)
            TransactionFileRepository.insert_transaction(transaction)
        except ValueError as e:
            print(f'{e}')

    @staticmethod
    def withdraw_(wallet_id):
        amount = input('Enter amount to withdraw: ')
        try:
            amount = float(amount)
            username = WalletFileRepository.withdrawal(wallet_id_=wallet_id, amount=amount)

            created_at = datetime.now().isoformat()
            transaction_id = str(created_at) + '-' + str(amount)
            receiver = ''
            sender = username
            transaction_type = 'debit'
            transaction = Transaction(transaction_id, created_at, sender, receiver, amount, transaction_type)
            TransactionFileRepository.insert_transaction(transaction)
        except ValueError as e:
            print(f'{e}')

    @staticmethod
    def send_money_(wallet_id):
        receiver = str(input('Enter recipient username: '))
        amount = input('Enter amount to send: ')
        try:
            amount = float(amount)
            username = WalletFileRepository.send_money(wallet_id, amount, receiver)

            created_at = datetime.now().isoformat()
            transaction_id = str(created_at) + '-' + str(amount)
            receiver = receiver
            sender = username
            transaction_type = 'debit'
            transaction = Transaction(transaction_id, created_at, sender, receiver, amount, transaction_type)
            TransactionFileRepository.insert_transaction(transaction)
        except ValueError  as e:
            print(f'{e}')

    @staticmethod
    def check_balance_(wallet_id):
        WalletFileRepository.check_balance(wallet_id)

    @staticmethod
    def profile_(wallet_id):
        WalletFileRepository.profile(wallet_id)
