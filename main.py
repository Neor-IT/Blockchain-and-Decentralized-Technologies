from binascii import unhexlify, hexlify
from time import time
import hashlib
import os


class Signature:
    def __init__(self):
        self.__data = {
            "public_key": "",
            "private_key": "",
            "signature": ""
        }

    def get_data(self):
        return self.__data

    def get_public_key(self):
        if self.__data['public_key'] == "":
            self.__data['public_key'] = hexlify(hashlib.sha256(unhexlify(self.__data['signature'])).digest()).decode('utf8')
        return self.__data['public_key']

    def generate_keys(self):
        self.__data['public_key'] = hexlify(os.urandom(32)).decode('utf8')
        self.__data['private_key'] = hexlify(os.urandom(32)).decode('utf8')

    def signature(self, message):
        self.__data['signature'] = hexlify(hashlib.sha256(unhexlify(message)).digest()).decode('utf8')


class KeyPair:
    def verify(self, message, signature):
        if hexlify(hashlib.sha256(unhexlify(message)).digest()).decode('utf8') == signature:
            return True
        else:
            return False


class Hash:
    def make_hash(self, prev_hash):
        hash = hexlify(hashlib.sha256(unhexlify(prev_hash)).digest()).decode('utf8')
        while hash[:5] != "00000":
            hash = hexlify(hashlib.sha256(unhexlify(hash)).digest()).decode('utf8')
        return hash


class Block:
    def __init__(self, prev_hash, transaction, amount):
        self.next = None

        self.__data = {
            "prev_hash": prev_hash,
            "transaction": transaction,
            "amount": amount,
            "hash": "",
            "time": time(),
            "verified": False
        }
        self.__data['hash'] = Hash().make_hash(self.get_data()['prev_hash'])

    def get_data(self):
        return self.__data

    def add_block(self, transaction, amount):
        block = self
        while block.next:
            block = block.next
        prev_hash = block.get_data()["hash"]
        end = Block(prev_hash, transaction, amount)
        block.next = end


def print_blocks(block):
    node = block
    print(node.get_data())

    while node.next:
        node = node.next
        print(node.get_data())


class Blockchain:
    def __init__(self):
        self.__data = {
            "blocks": []
        }

    def verify(self):
        for block in self.__data["blocks"]:

            Sign = Signature()
            Sign.generate_keys()
            Sign.signature(block["hash"])

            if block["verified"] is False:
                if KeyPair().verify(block["hash"], Sign.get_data()['signature']):
                    block["verified"] = True
                else:
                    print("Invalid block!")
                    break

    def append(self, block):
        node = block
        self.__data["blocks"].append(node.get_data())

        while node.next:
            node = node.next
            self.__data["blocks"].append(node.get_data())

    def print_blocks(self):
        for block in self.__data["blocks"]:
            if block["verified"] is True:
                print(block)


blockchain = Blockchain()
block = Block("0000000000000000000000000000000000000000000000000000000000000000", "Block #1", 0)


class Account:
    def __init__(self, username):
        self.username = username
        self.__data = {
            "balance": 0,
        }

    def get_data(self):
        return self.__data

    def add_balance(self, amount):
        self.__data['balance'] += amount

    def remove_balance(self, amount):
        self.__data['balance'] -= amount

    def transfer(self, amount, public_key):
        if self.__data['balance'] >= amount:
            self.remove_balance(amount)
            block.add_block(public_key, amount)
            blockchain.append(block)
            blockchain.verify()
        else:
            print("Not enough money!")

    def print_balance(self):
        print(f"Balance: {self.__data['balance']}")


Account = Account(Signature().get_public_key())
Account.add_balance(1000)
Account.transfer(500, "65345d332342f5d513bd9ae0672ff3c5ab7967b0e22e14d4b817601b68950643")
Account.print_balance()
blockchain.print_blocks()
