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
        return None
        
    def shingling_hash(self, shingling: str):
        return hash(shingling)
    
    def shingling(self, docs: str, k=9):
        docs_len = len(docs)
        shingling_set = set()
        for i in range(docs_len - k + 1):
            hash_result = self.shingling_hash(docs[i:i+k])
            shingling_set.add(hash_result)
        return shingling_set