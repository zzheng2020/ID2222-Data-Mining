"""
Authors: Chengyang Huang, Ziheng Zhang
Course:  ID2222 Data Mining
"""

"""
Compute Jaccard similarity of two sets of integers.
"""
class CompareSets():
    def __init__(self) -> None:
        return None
    
    def compare(self, set_a: set, set_b: set):
        union      = set_a.union(set_b)
        size_union = len(union)

        intersection      = set_a.intersection(set_b)
        size_intersection = len(intersection)

        return float(size_intersection / size_union)