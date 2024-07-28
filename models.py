from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Transaction:
    transaction_id: str
    created_at: str
    sender: str
    receiver: str
    amount: float
    transaction_type: str

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'created_at': self.created_at,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'transaction_type': self.transaction_type
        }


@dataclass
class User:
    name: str
    email: str
    phone: str
    username: str
    password: str
    created_at: str

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }


@dataclass
class Wallet:
    wallet_id: str
    balance: float
    username: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            'wallet_id': self.wallet_id,
            'balance': self.balance,
            'username': self.username,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
