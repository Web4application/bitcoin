from flask import Flask, render_template
from chain_Storage import load_chain_from_file

app = Flask(__name__)

@app.route('/')
def block_explorer():
    chain = load_chain_from_file()
    latest_hash = chain[-1].hash if chain else 'N/A'
    mining_status = "ACTIVE"  # You can toggle this dynamically later
    return render_template("block_explorer.html",
                           blocks=chain,
                           latest_hash=latest_hash,
                           chain_height=len(chain),
                           mining_status=mining_status)

if __name__ == '__main__':
    app.run(port=8080)
