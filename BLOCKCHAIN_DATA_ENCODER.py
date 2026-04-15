import base64
import zlib
import msgpack
import json
from typing import Any, Union

class BlockchainDataEncoder:
    @staticmethod
    def encode_json(data: dict) -> str:
        return json.dumps(data, sort_keys=True)

    @staticmethod
    def decode_json(encoded: str) -> dict:
        return json.loads(encoded)

    @staticmethod
    def encode_msgpack(data: Any) -> bytes:
        return msgpack.packb(data, use_bin_type=True)

    @staticmethod
    def decode_msgpack(encoded: bytes) -> Any:
        return msgpack.unpackb(encoded, raw=False)

    @staticmethod
    def compress_data(data: Union[str, bytes]) -> str:
        if isinstance(data, str):
            data = data.encode()
        compressed = zlib.compress(data)
        return base64.b64encode(compressed).decode()

    @staticmethod
    def decompress_data(encoded: str) -> str:
        decoded = base64.b64decode(encoded)
        decompressed = zlib.decompress(decoded)
        return decompressed.decode()

    @staticmethod
    def encode_transaction(tx: dict) -> str:
        json_str = BlockchainDataEncoder.encode_json(tx)
        compressed = BlockchainDataEncoder.compress_data(json_str)
        return compressed

    @staticmethod
    def decode_transaction(encoded: str) -> dict:
        decompressed = BlockchainDataEncoder.decompress_data(encoded)
        return BlockchainDataEncoder.decode_json(decompressed)
