import json

def get_private_data(filename: str):
    with open(filename) as file:
        data = json.load(file)

    return data