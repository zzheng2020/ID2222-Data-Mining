import math


class HyperLogLogCounter:
    def __init__(self, b=4):
        super().__init__()
        self.b = b
        self.m = 2 ** b
        self.M = [0] * self.m

        if b < 4 or b > 16:
            raise ValueError("b must be between 4 and 16")
        elif b == 4:
            self.alpha = 0.673
        elif b == 5:
            self.alpha = 0.697
        elif b == 6:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)

    def union(self, N: 'HyperLogLogCounter'):
        newCounter = HyperLogLogCounter(self.b)
        for i in range(newCounter.m):
            newCounter.M[i] = max(self.M[i], N.M[i])
        return newCounter

    def add(self, data):
        h = hash(data)
        # get the first b bits
        j = h & (self.m - 1)
        # get the remaining 32 - b bits
        w = h >> self.m
        # count the number of trailing 0s
        self.M[j] = max(self.M[j], Utils.rho(w) - self.m + 1)

    def cardinality(self):
        # fix when cardinality is 0
        if sum(self.M) == 0:
            return 0

        # print(self.M)
        # print(self.m / sum(2 ** -m for m in self.M))
        E = self.alpha * self.m ** 2 / sum(2 ** -m for m in self.M)
        if E <= 5 / 2 * self.m:
            V = self.m - self.M.count(0)
            if V != 0:
                E = self.m * math.log(self.m / V)
        elif E > 1 / 30 * 2 ** 32:
            E = -2 ** 32 * math.log(1 - E / 2 ** 32)
        return E


# logN space
class FMCounter:
    def __init__(self):
        super().__init__()
        self.bitset = 0  # we use a 64bit bitset
        self.phi = 0.77351

    def add(self, data: int):
        self.bitset |= Utils.lowbit(data)

    def cardinality(self):
        num = self.bitset
        estimate = 1
        while num > 0:
            estimate *= 2
            num >>= 1
        return int(estimate / self.phi)


# loglogN space
class FMCounter2:
    def __init__(self):
        super().__init__()
        self.maxBit = 0
        self.phi = 0.77351

    def add(self, data):
        self.maxBit = max(self.maxBit, Utils.lowbit(hash(data)))

    def cardinality(self):
        num = self.maxBit
        estimate = 1
        cnt = 0
        while num > 0:
            cnt += 1
            estimate *= 2
            num >>= 1
        print(cnt)
        return int(estimate / self.phi)


class Utils:
    # required by FMCounter
    @staticmethod
    def lowbit(x):
        return x & (-x)

    # required by HyperLogLog
    @staticmethod
    def rho(x):
        if x == 0:
            return 64
        n = 0
        if (x >> 32) == 0:
            n += 32
            x <<= 32
        if (x >> 48) == 0:
            n += 16
            x <<= 16
        if (x >> 56) == 0:
            n += 8
            x <<= 8
        if (x >> 60) == 0:
            n += 4
            x <<= 4
        if (x >> 62) == 0:
            n += 2
            x <<= 2
        if (x >> 63) == 0:
            n += 1
        return n


if __name__ == "__main__":
    # fmp = FMCounter2()
    counter = HyperLogLogCounter()

    with open("web-Google.txt", "r") as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            if line.startswith("#"):
                continue
            data = line.strip().split()
            counter.add(str(data[0]))
            counter.add(str(data[1]))
        print(counter.cardinality())