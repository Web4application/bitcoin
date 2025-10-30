import json

def save_chain(chain):
    with open("chain_data.json", "w") as file:
        json.dump(chain, file)

def load_chain():
    try:
        with open("chain_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
