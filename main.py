from binascii import unhexlify, hexlify
from time import time
import hashlib
import random
import math


class KeyPair:

    @staticmethod
    def __isPrime(n):
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        i = 3
        while i <= math.sqrt(n):
            if n % i == 0:
                return False
            i += 2
        return True

    def __generate_prime(self, a=0, b=1000):
        num = 0
        while self.__isPrime(num) is False:
            num = random.randint(a, b)
        return num

    @staticmethod
    def __gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    def __keyGen(self):
        p = self.__generate_prime()
        q = self.__generate_prime()
        n = p * q

        phi = (p - 1) * (q - 1)
        e = random.randint(1, phi)
        g = self.__gcd(e, phi)

        while g != 1:
            e = random.randint(1, phi)
            g = self.__gcd(e, phi)

        d = pow(e, -1, phi)
        return (e, n), (d, n)

    def genKeyPair(self):
        self.privateKey, self.publicKey = self.__keyGen()
        return self.privateKey, self.publicKey


class Signature:

    @staticmethod
    def signData(message, primary_key):
        key, n = primary_key
        return [pow(ord(char), key, n) for char in message]

    def verifySignature(self, message, signature, primary_key):
        key, n = primary_key
        return ''.join([chr(pow(char, key, n)) for char in signature]) == message


class Hash:

    @staticmethod
    def make_hash(prev_hash):
        hash = hexlify(hashlib.sha256(unhexlify(prev_hash)).digest()).decode('utf8')
        while hash[:5] != "00000":
            hash = hexlify(hashlib.sha256(unhexlify(hash)).digest()).decode('utf8')
        return hash


class Account:  # improved in the future
    def __init__(self):
        self.__accountID = 0
        self.__wallet = []
        self.__balance = 20

        self.obj = {
            "accountID": self.__accountID,
            "wallet": self.__wallet,
            "balance": self.__balance
        }

    def genAccount(self, private_key, public_key):
        self.__accountID = random.randint(0, int(time()))
        self.__wallet.append(private_key)
        self.__wallet.append(public_key)

    def addKeyPairToWallet(self) -> None:
        private, public = KeyPair().genKeyPair()
        self.wallet = [private, public]

    def updateBalance(self, amount) -> None:
        self.__balance += amount

    def createPaymentOp(self, amount, receiver):
        data = {
            "sender": self.obj["accountID"],
            "receiver": receiver,
            "amount": amount,
            "data": self.signData(str(self.obj["accountID"]) + str(amount) + str(receiver), 0)
        }

        self.updateBalance(-amount)

        return data

    def getBalance(self) -> int:
        return self.__balance

    def printBalance(self):
        print(self.__balance)

    def signData(self, message, index):
        return Signature().signData(message, self.__wallet[index])


class Operation:  # improved in the future
    def __init__(self):
        self.sender = None
        self.receiver = None
        self.amount = None
        self.signature = None

        self.__data = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature
        }

    def createOperation(self, sender, receiver, amount, signature):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def verifyOperation(self, public_key, payment_op: dict):
        if Signature().verifySignature(str(payment_op["sender"]) + str(payment_op["amount"]) + str(payment_op["receiver"]),
                                      payment_op["data"], public_key):
            if payment_op["amount"] <= Account().getBalance():
                return True

        return False


class Transaction:  # improved in the future
    def __init__(self):
        self.transactionID = None
        self.setOfOperations = []

    def createOperation(self, operation, nonce):
        self.transactionID = Hash().make_hash(str(operation) + str(nonce))
        self.setOfOperations.append(operation)


class Block:  # improved in the future
    def __init__(self):
        self.blockID = None
        self.prevHash = None
        self.setOfTransactions = []

    def createBlock(self, prev_hash, nonce):
        self.blockID = Hash().make_hash(str(prev_hash) + str(nonce))
        self.prevHash = prev_hash


class Blockchain:  # improved in the future
    def __init__(self):
        self.coinDatabase = {}
        self.blockHistory = []
        self.txDatabase = []
        self.faucetCoins = None

    def initBlockchain(self, faucetCoins):
        self.faucetCoins = faucetCoins
        self.blockHistory.append(Block().createBlock("0", 0))
        self.coinDatabase[0] = faucetCoins

    def getTokenFromFaucet(self, accountID):
        self.coinDatabase[accountID] = self.faucetCoins

    def validateBlock(self, block):
        if block.blockID == Hash().make_hash(str(block.prevHash) + str(0)):
            return True
        return False

    def getBalance(self, accountID):
        return self.coinDatabase[accountID]
    

if __name__ == '__main__':
    private, public = KeyPair().genKeyPair()

    signature = Signature().signData(input('Enter a message: '), private)
    print('Verify signature:', Signature().verifySignature(input("Enter a message: "), signature, public))
