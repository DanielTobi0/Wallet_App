from datetime import datetime


class Transaction:
    def __init__(self, transaction_id, created_at, sender, receiver, amount, transaction_type):
        self.transaction_id = transaction_id
        self.created_at = created_at
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.transaction_type = transaction_type

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'created_at': self.created_at,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'transaction_type': self.transaction_type
        }


class User:
    def __init__(self, name, email, phone, username, password, created_at):
        self.name = name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
        self.created_at = created_at

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }


class Wallet:
    def __init__(self, wallet_id, balance, username, **kwargs):
        self.wallet_id = wallet_id
        self.balance: float = balance
        self.username = username
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'wallet_id': self.wallet_id,
            'balance': self.balance,
            'username': self.username,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }