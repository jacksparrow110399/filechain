import time
import hashlib

class Block:
    def __init__(self, index, timestamp, filename, file_hash, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.filename = filename
        self.file_hash = file_hash
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.filename}{self.file_hash}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "filename": self.filename,
            "file_hash": self.file_hash,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(data):
        block = Block(
            data['index'],
            data['timestamp'],
            data['filename'],
            data['file_hash'],
            data['previous_hash']
        )
        block.hash = data['hash']
        return block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, filename, file_hash):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            filename=filename,
            file_hash=file_hash,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)

    def get_chain(self):
        return [block.to_dict() for block in self.chain]

    def load_chain(self, chain_data):
        self.chain = [Block.from_dict(block) for block in chain_data]

