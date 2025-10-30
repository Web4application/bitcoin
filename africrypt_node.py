# africrypt_node.py

from flask import Flask, request, jsonify
from blockchain import Block, Transaction, proof_of_work
from chain_Storage import load_chain_from_file, save_chain_to_file
from registry_server import register_node, fetch_peers
from cli_dashboard import show_dashboard
import threading
import time

app = Flask(__name__)

# Load chain and pending transaction pool
chain = load_chain_from_file()
tx_pool = []
peers = []

# 🏁 Auto-mining toggle
auto_mining = True

def auto_mine():
    while auto_mining:
        if tx_pool:
            new_block = Block(len(chain), tx_pool[:], chain[-1].hash)
            mined_block = proof_of_work(new_block)
            chain.append(mined_block)
            save_chain_to_file(chain)
            tx_pool.clear()
            print(f"✅ Mined block #{mined_block.index}")
        time.sleep(10)

# 📡 Peer sync on startup
def sync_peers():
    register_node("http://localhost:5000")
    global peers
    peers = fetch_peers()

# 🧾 Transaction endpoint
@app.route('/send_tx', methods=['POST'])
def receive_transaction():
    data = request.get_json()
    tx = Transaction(**data)
    if tx.verify_signature():
        tx_pool.append(tx)
        return jsonify({"status": "Transaction added"}), 200
    return jsonify({"error": "Invalid transaction signature"}), 400

# ⛓ Chain endpoint
@app.route('/chain', methods=['GET'])
def serve_chain():
    return jsonify([block.__dict__ for block in chain]), 200

# 📡 Block broadcast
@app.route('/broadcast_block', methods=['POST'])
def receive_block():
    data = request.get_json()
    # Validate & merge block logic can go here
    chain.append(Block(**data))  # Simplified
    save_chain_to_file(chain)
    return jsonify({"status": "Block received"}), 200

@app.route('/peers', methods=['GET'])
def serve_peers():
    return jsonify(peers), 200

# 🚀 Start everything
if __name__ == '__main__':
    sync_peers()
    threading.Thread(target=auto_mine, daemon=True).start()
    threading.Thread(target=lambda: show_dashboard(chain, tx_pool, peers), daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
