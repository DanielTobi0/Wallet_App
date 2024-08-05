from datetime import datetime
from dataclasses import dataclass, field


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
