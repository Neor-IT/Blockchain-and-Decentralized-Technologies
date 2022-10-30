class Sha1:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __chunks(k, m):
        return [k[i:i + m] for i in range(0, len(k), m)]

    @staticmethod
    def __rol(i, j):
        return ((i << j) | (i >> (32 - j))) & 0xffffffff

    def sha1(self):
        bytes = ""

        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0

        for i in range(len(self.data)):
            bytes += f"{ord(self.data[i]):08b}"
        bits = bytes + "1"
        _bits = bits

        while len(_bits) % 512 != 448:
            _bits += "0"

        _bits += f"{len(bits) - 1:064b}"

        for chunk in self.__chunks(_bits, 512):
            words = self.__chunks(chunk, 32)
            w = [0] * 80

            for i in range(0, 16):
                w[i] = int(words[i], 2)

            for j in range(16, 80):
                w[j] = self.__rol((w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16]), 1)

            a = h0
            b = h1
            chunk = h2
            d = h3
            e = h4
            f, k = 0, 0

            for i in range(0, 80):

                if 0 <= i <= 19:
                    f = (b & chunk) | ((~b) & d)
                    k = 0x5A827999

                elif 20 <= i <= 39:
                    f = b ^ chunk ^ d
                    k = 0x6ED9EBA1

                elif 40 <= i <= 59:
                    f = (b & chunk) | (b & d) | (chunk & d)
                    k = 0x8F1BBCDC

                elif 60 <= i <= 79:
                    f = b ^ chunk ^ d
                    k = 0xCA62C1D6

                temp = self.__rol(a, 5) + f + e + k + w[i] & 0xffffffff
                e = d
                d = chunk

                chunk = self.__rol(b, 30)
                b = a
                a = temp

            h0 = h0 + a & 0xffffffff
            h1 = h1 + b & 0xffffffff
            h2 = h2 + chunk & 0xffffffff
            h3 = h3 + d & 0xffffffff
            h4 = h4 + e & 0xffffffff

        return "%08x%08x%08x%08x%08x" % (h0, h1, h2, h3, h4)


if __name__ == "__main__":
    print(Sha1("Hello, world!").sha1())  # 943a702d06f34599aee1f8da8ef9f7296031d699
    print(Sha1("hello").sha1() == "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")  # True
    print(Sha1("Hello, world!").sha1() == "943a702d06f34599aee1f8da8ef9f7296031d699")  # True
