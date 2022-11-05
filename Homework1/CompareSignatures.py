"""
Authors: Chengyang Huang, Ziheng Zhang
Course:  ID2222 Data Mining
"""

"""
Compute similarity between two documents using minHash signatures.
"""

from typing import List


class CompareSignatures:
    def similarity(self, sig1: List[int], sig2: List[int]) -> float:
        if len(sig1) != len(sig2):
            raise Exception("Signature size not match")
        return sum([1 if sig1[i] == sig2[i] else 0 for i in range(len(sig1))]) / len(sig1)
