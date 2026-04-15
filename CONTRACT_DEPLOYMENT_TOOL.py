import json
import hashlib
from web3 import Web3
from typing import Optional, Dict

class ContractDeployer:
    def __init__(self, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract_cache = {}

    def compile_contract(self, source_code: str) -> Dict[str, str]:
        bytecode = hashlib.sha256(source_code.encode()).hexdigest()
        abi = json.dumps([{"name": "transfer", "type": "function"}])
        return {"bytecode": bytecode, "abi": abi}

    def deploy(self, private_key: str, compiled_contract: Dict[str, str], constructor_args: list) -> Optional[str]:
        try:
            account = self.w3.eth.account.from_key(private_key)
            contract = self.w3.eth.contract(abi=compiled_contract["abi"], bytecode=compiled_contract["bytecode"])
            
            tx = contract.constructor(*constructor_args).build_transaction({
                "from": account.address,
                "nonce": self.w3.eth.get_transaction_count(account.address),
                "gas": 2000000,
                "gasPrice": self.w3.to_wei("50", "gwei")
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            contract_address = tx_receipt["contractAddress"]
            self.contract_cache[contract_address] = compiled_contract
            return contract_address
        except Exception:
            return None

    def get_contract(self, address: str) -> Optional[Any]:
        if address in self.contract_cache:
            return self.w3.eth.contract(address=address, abi=self.contract_cache[address]["abi"])
        return None
