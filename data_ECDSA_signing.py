from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib
import time

class Transaction:
    def __init__(self, sender_pub_key, recipient_address, amount, sender_priv_key):
        self.sender_pub_key = sender_pub_key.to_string().hex()
        self.recipient = recipient_address
        self.amount = amount
        self.timestamp = time.time()
        self.signature = self.sign_transaction(sender_priv_key)

    def transaction_data(self):
        return f"{self.sender_pub_key}->{self.recipient}:{self.amount}:{self.timestamp}"

    def sign_transaction(self, private_key):
        tx_hash = hashlib.sha256(self.transaction_data().encode()).digest()
        signature = private_key.sign(tx_hash)
        return signature.hex()

    def verify_signature(self):
        tx_hash = hashlib.sha256(self.transaction_data().encode()).digest()
        pub_key_bytes = bytes.fromhex(self.sender_pub_key)
        pub_key = VerifyingKey.from_string(pub_key_bytes, curve=SECP256k1)
        return pub_key.verify(bytes.fromhex(self.signature), tx_hash)
