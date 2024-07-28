import json


class UserUtils:

    @staticmethod
    def load():
        pass


class WalletUtils:
    @staticmethod
    def load():
        pass


def load_data(path, model):
    try:
        with open(path, 'r') as data_file:
            data_dicts = json.load(data_file)
        if not data_dicts:
            return []
        return [model(**data_dict) for data_dict in data_dicts]
    except FileNotFoundError:
        print(f'{model.__name__} DB not found, creating one now')
        open(path, 'x').close()
        return []
    except json.JSONDecodeError:
        print(f'{model.__name__} DB is empty or corrupted')
        return []


def write_to_db(path, data):
    try:
        with open(path, 'w') as file:
            json.dump([d.to_dict() for d in data], file, indent=4, sort_keys=True, default=str)
    except FileNotFoundError:
        print(f'{data} DB not found, creating one now')
