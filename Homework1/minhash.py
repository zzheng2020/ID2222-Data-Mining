"""
Authors: Chengyang Huang, Ziheng Zhang
Course:  ID2222 Data Mining
"""

"""
Compute minHash signatures from one ordered hashed shingling.
"""

from typing import List
import random
import math


class MinHashing:
    def __init__(self, nHash: int, maxShinglingSize: int):
        hashSt = set()
        while len(hashSt) < nHash:
            # a, b, mod
            hashSt.add((random.randint(0, maxShinglingSize),
             random.randint(0, maxShinglingSize)))
        self.hashs = list(hashSt)
        # or alternatively we can just use the maximum hashed shingle
        self.mod = self.nxtPrime(maxShinglingSize)
    
    def isPrime(self, n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i = i + 6
        return True

    def nxtPrime(self, n):
        if n <= 1:
            return 2
        while True:
            if self.isPrime(n):
                return n
            n += 1

    def signature(self, hashedShingling: List[int]) -> List[int]:
        minHashSignature = [math.inf for _ in range(len(self.hashs))]
        for i, (a, b) in enumerate(self.hashs):
            # for all occured postions in hashed space
            for hashedShingle in hashedShingling:
                hashedShingle = (a * hashedShingle + b) % self.mod
                minHashSignature[i] = min(minHashSignature[i], hashedShingle)
        return minHashSignature

if __name__ == "__main__":
    shinglings = [[0, 3], [2], [1, 3, 4], [0, 2, 3]]
    mh = MinHashing(2, 5)
    mh.mod = 5
    mh.hashs = [(1, 1), (3, 1)]
    print(list(map(mh.signature, shinglings)))
    # expected [[1, 0], [3, 2], [0, 0], [1, 0]]
