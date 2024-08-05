from dataclasses import dataclass


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