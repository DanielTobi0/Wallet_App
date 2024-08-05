from dataclasses import dataclass


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
