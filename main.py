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

    def __generatePrime(self, a=0, b=1000):
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
        p = self.__generatePrime()
        q = self.__generatePrime()
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


class Account:
    def __init__(self):
        self.__accountID = 0
        self.__wallet = []
        self.__balance = 0

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


class Operation:
    def __init__(self):
        self.sender = None
        self.receiver = None
        self.amount = None
        self.signature = None
        self.hash = None

    def createOperation(self, sender, receiver, amount, signature, prev_hash):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
        print("Calculating hash...")
        self.hash = Hash().toHash(prev_hash)

        self.data = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature,
            "prev_hash": prev_hash,
            "hash": self.hash
        }

        return self.data

    def verifyOperation(self, public_key, payment_op: dict):
        return Signature().verifySignature(str(payment_op["sender"]) + str(payment_op["amount"]) + str(payment_op["receiver"]),
                                           payment_op["signature"], public_key)


class Transaction:
    def __init__(self):
        self.transactionID = None
        self.setOfOperations = []

    def makeNonce(self):
        return hash(random.randint(0, int(time())))

    def createOperation(self, operation, nonce):
        self.setOfOperations.append(operation)
        self.transactionID = abs(hash(str(self.setOfOperations) + str(nonce)))
        print("Nonce:", nonce)
        # print("setOfOperations:", self.setOfOperations)
        return self.setOfOperations


class Hash:
    @staticmethod
    def toHash(prev_hash):
        print("PREV_HASH:", prev_hash)
        hash = hexlify(hashlib.sha256(unhexlify(prev_hash)).digest()).decode('utf8')
        while hash[:5] != "00000":
            hash = hexlify(hashlib.sha256(unhexlify(hash)).digest()).decode('utf8')
        return hash


class Block:
    def __init__(self):
        self.blockID = None
        self.prevHash = None
        self.setOfTransactions = []

    def createBlock(self, prev_hash, transaction):
        self.blockID = abs(hash(str(transaction) + str(prev_hash)))
        self.prevHash = prev_hash
        self.setOfTransactions.append(transaction)

        return self.setOfTransactions


class Blockchain:
    def __init__(self):
        self.coinDatabase = {}
        self.blockHistory = []
        self.txDatabase = []
        self.faucetCoins = 100

    def initBlockchain(self):
        genesisBlock = Block().createBlock("0", Transaction().createOperation(
            Operation().createOperation(None, 1, self.faucetCoins, None, '0000000000000000000000000000000000000000000000000000000000000000'), Transaction().makeNonce()))
        self.blockHistory.append(genesisBlock)
        self.coinDatabase[1] = self.faucetCoins

        return self.blockHistory

    def getTokenFromFaucet(self, account):
        account.genAccount(*KeyPair().genKeyPair())
        account.updateBalance(self.faucetCoins)
        self.coinDatabase[account.obj["accountID"]] = account

        return account

    def validateBlock(self, block: Block, prev_hash, public_key):
        if block.prevHash != prev_hash:
            print("Block is not valid")
            return False

        for transaction in block.setOfTransactions:
            for operation in transaction:
                # print(operation)
                if Operation().verifyOperation(public_key, operation):
                    print("Operation is not valid")
                    return False
                print("balance", self.coinDatabase[operation["sender"]].getBalance())
                if not self.coinDatabase[operation["sender"]].getBalance() >= operation["amount"]:
                    print("Not enough coins")
                    return False

        self.blockHistory.append(block)
        return True

    def getBalanceFromFaucet(self, account):
        return self.getTokenFromFaucet(account).getBalance()


if __name__ == '__main__':
    private, public = KeyPair().genKeyPair()
    # print("private, public keys:", private, public)

    # signature = Signature().signData("message", private)
    # print('Verify signature:', Signature().verifySignature("message", signature, public))

    account = Account()
    account.genAccount(private, public)
    # print("Account:", account.obj)
    # print("Balance:", account.getBalance())

    blockchain = Blockchain()
    blockchain.initBlockchain()
    # print("Blockchain:", blockchain.blockHistory)
    genesis_hash = blockchain.blockHistory[0][0][0]["hash"]
    # get token from faucet
    blockchain.getBalanceFromFaucet(account)
    # print("Balance:", account.getBalance())

    # create transaction
    operation = Operation()
    data = operation.createOperation(account.obj["accountID"], "receiver", 10, public, genesis_hash)
    # print("data", data)
    transaction = Transaction()
    transaction.createOperation(data, transaction.makeNonce())
    # print("Transaction:", transaction.setOfOperations)

    block = Block()
    # create block
    block.createBlock(blockchain.blockHistory[-1], transaction.setOfOperations)
    # print(transaction.setOfOperations)
    # print("Block:", block.setOfTransactions)

    # validate block
    validate = blockchain.validateBlock(block, blockchain.blockHistory[-1], public)
    if validate:
        print("Block is valid")
        print(block.setOfTransactions)
        for transaction in block.setOfTransactions:
            for operation in transaction:
                print(operation)
        account.createPaymentOp(operation["amount"], operation["receiver"])

    # print("Blockchain:", blockchain.blockHistory)
    # print("Coin database:", blockchain.coinDatabase)
    print("Balance:", account.getBalance())

    # create transaction
    operation = Operation()
    data = operation.createOperation(account.obj["accountID"], "receiver", 10, public, data["hash"])
    # print("data", data)
    transaction = Transaction()
    transaction.createOperation(data, transaction.makeNonce())
    # print("Transaction:", transaction.setOfOperations)

    block = Block()
    # create block
    block.createBlock(blockchain.blockHistory[-1], transaction.setOfOperations)
    # print(transaction.setOfOperations)
    # print("Block:", block.setOfTransactions)

    # validate block
    validate = blockchain.validateBlock(block, blockchain.blockHistory[-1], public)
    if validate:
        print("Block is valid")
        print(block.setOfTransactions)
        for transaction in block.setOfTransactions:
            for operation in transaction:
                print(operation)
        account.createPaymentOp(operation["amount"], operation["receiver"])

    print("Blockchain:", blockchain.blockHistory)
    print("Balance:", account.getBalance())
