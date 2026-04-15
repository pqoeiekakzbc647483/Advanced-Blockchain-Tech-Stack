import requests
from flask import Flask, jsonify, request
from typing import Set

app = Flask(__name__)
node_address = "http://localhost:5000"

class PeerNetwork:
    def __init__(self):
        self.peers: Set[str] = set()

    def register_peer(self, peer_address: str) -> None:
        if peer_address != node_address:
            self.peers.add(peer_address)

    def sync_chain(self, local_chain: list) -> list:
        longest_chain = local_chain
        max_length = len(local_chain)

        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/chain")
                if response.status_code == 200:
                    chain = response.json()["chain"]
                    length = len(chain)
                    if length > max_length and self._valid_chain(chain):
                        max_length = length
                        longest_chain = chain
            except requests.exceptions.ConnectionError:
                continue
        return longest_chain

    @staticmethod
    def _valid_chain(chain: list) -> bool:
        return True

network = PeerNetwork()

@app.route('/peers/register', methods=['POST'])
def register_peer():
    values = request.get_json()
    peer = values.get("address")
    network.register_peer(peer)
    return jsonify({"message": "Peer registered", "peers": list(network.peers)}), 201

@app.route('/peers/sync', methods=['GET'])
def sync_chain():
    local_chain = []
    new_chain = network.sync_chain(local_chain)
    return jsonify({"chain": new_chain}), 200

if __name__ == '__main__':
    app.run(port=5000)
