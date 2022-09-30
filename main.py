import hashlib
from time import time
from random import choice
import itertools


class Blockchain:
    def __init__(self):
        self.alphabet = '0123456789abcdef'
        self.prev_hash = ''
        self.keys = 0
        self.hash = ''

    def __make_hash(self):
        hash = hashlib.sha256()
        hash.update((str(time()).join([choice(self.alphabet) for _ in range(len(str(self.keys)))])).encode('utf-8'))
        return hash.hexdigest()[:len(str(self.keys))]

    def __get_hash(self):
        hash_key = self.__make_hash()
        while len(hash_key) < len(str(self.keys)):
            hash_key += self.__make_hash()
        hash = f"0x{hash_key}"
        return hash

    def __brute(self):
        time_start = time()
        self.prev_hash = self.hash[2:]
        self.prev_hash = tuple(self.prev_hash)
        char_list = [[x for x in self.alphabet]] * len(self.prev_hash)

        for combination in itertools.product(*char_list):
            if combination == self.prev_hash:
                hash = "0x" + "".join(combination)
                print(f"Хеш {hash} забручений за {round((time() - time_start) * 1000)} ms!")

    def main(self, length: int = 8):
        while length <= 4096:
            self.keys = 2 ** length
            print(f"{length} bits\nПростір ключів: {self.keys}")
            length *= 2
            self.hash = self.__get_hash()
            print("HASH:", self.hash)
            choice = input("Бажаєте почати brute force цього хешу? (y/n): ").lower()
            if choice == 'y':
                self.__brute()
            print("\n")


Block = Blockchain()
Block.main()
