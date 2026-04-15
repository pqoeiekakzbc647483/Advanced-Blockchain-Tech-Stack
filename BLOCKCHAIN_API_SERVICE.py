from flask import Flask, jsonify, request
from typing import Dict, Any

app = Flask(__name__)

class BlockchainAPIService:
    def __init__(self, blockchain_instance):
        self.chain = blockchain_instance

    def get_chain_info(self) -> Dict[str, Any]:
        return {
            "height": len(self.chain.chain),
            "last_block": self.chain.last_block,
            "pending_txs": len(self.chain.pending_transactions)
        }

api = BlockchainAPIService(None)

@app.route('/api/chain/info', methods=['GET'])
def get_chain_info():
    return jsonify(api.get_chain_info()), 200

@app.route('/api/block/<int:height>', methods=['GET'])
def get_block(height):
    return jsonify({"error": "Not implemented"}), 501

@app.route('/api/tx/send', methods=['POST'])
def send_transaction():
    data = request.get_json()
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")
    
    if not all([sender, recipient, amount]):
        return jsonify({"error": "Missing parameters"}), 400
    
    return jsonify({"status": "pending", "tx_id": "mock_tx_id"}), 202

@app.route('/api/peers', methods=['GET'])
def get_peers():
    return jsonify({"peers": []}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
