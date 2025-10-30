from ecdsa import SigningKey, SECP256k1

# Generate wallet key pair
def generate_wallet():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key
