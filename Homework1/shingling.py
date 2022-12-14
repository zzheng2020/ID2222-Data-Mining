"""
Authors: Chengyang Huang, Ziheng Zhang
Course:  ID2222 Data Mining
"""

"""
Constructs k-shingles of a given length k (default: k=9) from a given document,
computes a hash value for each unique shingle and represents the document
in the form of an ordered set of its hashed k-shingles.
"""
class Shingling():
    def __init__(self) -> None:
        self._max_hashvalue = (1 << 32) - 1
        return None

    def shingling_hash(self, shingling: str):
        hash_value = hash(shingling)
        if hash_value < 0:
            return (self._max_hashvalue + hash_value) % self._max_hashvalue
        else:
            return hash_value % self._max_hashvalue

    def shingling(self, docs: str, k=9):
        docs_len = len(docs)
        shingling_set = set()
        for i in range(docs_len - k + 1):
            hash_result = self.shingling_hash(docs[i:i+k])
            shingling_set.add(hash_result)
        return sorted(shingling_set)
