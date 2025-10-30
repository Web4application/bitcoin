import hashlib
import time
import json

class GenesisBlock:
    def __init__(self):
        self.index = 0
        self.timestamp = time.time()
        self.data = {
            "chain_name": "AfriCryptChain",
            "creator": "kubu",
            "message": "Powering Crypto Innovation Across the Continent",
            "initial_supply": 100000000,  # total AFCT tokens
            "genesis_address": "AFCT1KUBU00000000000000000000"
        }
        self.previous_hash = "0" * 64
        self.nonce = 0
        self.hash = self.calculate_hash()
 
    class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = [tx.__dict__ for tx in transactions if tx.verify_signature()]
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

genesis = GenesisBlock()
print("🔓 AfriCryptChain Genesis Block Created:")
print(f"Hash: {genesis.hash}")
print(f"Block Data: {genesis.data}")

def proof_of_work(block, difficulty=4):
    prefix = "0" * difficulty
    while not block.calculate_hash().startswith(prefix):
        block.nonce += 1
        block.hash = block.calculate_hash()
    return block
def robust_sync(peer):
    for attempt in range(5):
        try:
            res = requests.get(f"http://{peer}/chain", timeout=3)
            if res.status_code == 200:
                update_chain(res.json())
                return True
        except:
            time.sleep(2 ** attempt)
    return False

def save_chain_to_file(chain):
    with open("chain.json", "w") as f:
        json.dump(chain, f)

def load_chain_from_file():
    try:
        with open("chain.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
