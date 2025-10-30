from ecdsa import SigningKey, SECP256k1
import hashlib

# Generate key pair
private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key()

# Sample transaction data
tx_data = "AFCT1KUBU00001->AFCT1MARK00002:250"

# Hash the data
tx_hash = hashlib.sha256(tx_data.encode()).digest()

# Sign it
signature = private_key.sign(tx_hash)
print(f"Signature: {signature.hex()}")
