import hashlib
import time

class Block:
    def __init__(self, index, filename, file_hash, timestamp, previous_hash):
        self.index = index
        self.filename = filename
        self.file_hash = file_hash
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = f"{self.index}{self.filename}{self.file_hash}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "Genesis", "0"*64, time.time(), "0")
        self.chain.append(genesis)

    def add_block(self, filename, file_hash):
        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            filename=filename,
            file_hash=file_hash,
            timestamp=time.time(),
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)

    def get_chain(self):
        return self.chain
