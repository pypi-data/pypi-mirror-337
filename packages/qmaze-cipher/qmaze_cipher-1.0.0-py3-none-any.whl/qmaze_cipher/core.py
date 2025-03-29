import hashlib
import base64
import os

class QMazeCipher:
    def __init__(self, key, chaos_r=3.99, block_size=16):
        self.key = key.encode()
        self.chaos_r = chaos_r
        self.block_size = block_size

    def _hash_key(self, key_material):
        return hashlib.sha3_256(key_material).digest()

    def _logistic_map_sequence(self, seed, length):
        x = seed
        seq = []
        for _ in range(length):
            x = self.chaos_r * x * (1 - x)
            seq.append(x)
        return seq

    def _permute_block(self, block, chaos_seq):
        index_map = sorted(range(len(block)), key=lambda i: chaos_seq[i])
        return bytes([block[i] for i in index_map])

    def _unpermute_block(self, block, chaos_seq):
        index_map = sorted(range(len(block)), key=lambda i: chaos_seq[i])
        reverse_map = [0] * len(block)
        for idx, orig_idx in enumerate(index_map):
            reverse_map[orig_idx] = idx
        return bytes([block[reverse_map[i]] for i in range(len(block))])

    def _pad(self, data):
        pad_len = self.block_size - (len(data) % self.block_size)
        return data + bytes([pad_len]) * pad_len

    def _unpad(self, data):
        pad_len = data[-1]
        if pad_len < 1 or pad_len > self.block_size:
            raise ValueError("Invalid padding")
        if data[-pad_len:] != bytes([pad_len]) * pad_len:
            raise ValueError("Corrupted padding")
        return data[:-pad_len]

    def encrypt(self, plaintext):
        nonce = os.urandom(8)
        data = self._pad(plaintext.encode())
        blocks = [data[i:i + self.block_size] for i in range(0, len(data), self.block_size)]
        ciphertext = b""

        for i, block in enumerate(blocks):
            dynamic_key = self._hash_key(self.key + nonce + i.to_bytes(2, 'big'))
            xor_block = bytes([b ^ dynamic_key[j % len(dynamic_key)] for j, b in enumerate(block)])
            seed = sum(dynamic_key) % 1000 / 1000
            chaos_seq = self._logistic_map_sequence(seed, self.block_size)
            permuted = self._permute_block(xor_block, chaos_seq)
            ciphertext += permuted

        return base64.urlsafe_b64encode(nonce + ciphertext).decode()

    def decrypt(self, encoded_ciphertext):
        raw = base64.urlsafe_b64decode(encoded_ciphertext)
        nonce, ciphertext = raw[:8], raw[8:]
        blocks = [ciphertext[i:i + self.block_size] for i in range(0, len(ciphertext), self.block_size)]
        plaintext = b""

        for i, block in enumerate(blocks):
            dynamic_key = self._hash_key(self.key + nonce + i.to_bytes(2, 'big'))
            seed = sum(dynamic_key) % 1000 / 1000
            chaos_seq = self._logistic_map_sequence(seed, self.block_size)
            unpermuted = self._unpermute_block(block, chaos_seq)
            xor_block = bytes([b ^ dynamic_key[j % len(dynamic_key)] for j, b in enumerate(unpermuted)])
            plaintext += xor_block

        try:
            return self._unpad(plaintext).decode()
        except Exception:
            raise ValueError("Invalid or corrupted ciphertext")
