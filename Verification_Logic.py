# Verifying signature
try:
    is_valid = public_key.verify(signature, tx_hash)
    print("✅ Transaction signature is valid!") if is_valid else print("❌ Invalid signature")
except:
    print("❌ Signature verification failed")
