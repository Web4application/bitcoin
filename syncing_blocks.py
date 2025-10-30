import requests, time

def sync_with_peer(peer_url, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            response = requests.get(f"http://{peer_url}/chain", timeout=3)
            if response.status_code == 200:
                print("✅ Synced with peer")
                return response.json()
        except Exception:
            print(f"⏳ Retrying... attempt {attempt+1}")
            time.sleep(2 ** attempt)
            attempt += 1
    print("❌ Peer unreachable.")
    return None
