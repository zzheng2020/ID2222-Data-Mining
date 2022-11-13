"""
Authors: Chengyang Huang, Ziheng Zhang
Course:  ID2222 Data Mining
"""

import collections
import typing

import apriori_utils as utl


class APriori:
    def __init__(self, file_path, min_support, min_confidence):
        self.file_path = file_path
        self.min_support = min_support
        self.min_confidence = min_confidence

        """
        预处理每个元素在第几行
        dict: key=item, value=line_number
        e.g. item2line_index[1] = (0, 1 ,2) 表示元素 1 在第 0, 1, 2 行出现过
        """
        self.item2line_index = collections.defaultdict(set)
        self.total_line = 1  # 总共这么多行
        with open(self.file_path) as f:
            for line in f:
                line_tuple = ()
                for i in line.strip().split(' '):
                    line_tuple += (i,)
                    self.item2line_index[i].add(self.total_line)
                self.total_line += 1
        f.close()

    def items_index(self, itemset):
        itemset = sorted(itemset, key=lambda item: len(self.item2line_index[item]), reverse=True)

        item = itemset.pop()
        index = self.item2line_index[item]
        support = len(index) / self.total_line

        # frequent set 中的元素必须每个都满足要求
        if support < self.min_support:
            return False, None

        while itemset:
            item = itemset.pop()

            # 两个元素共同出现在了哪些行, 并且判断是否满足要求
            index = index.intersection(self.item2line_index[item])
            support = len(index) / self.total_line
            if support < self.min_support:
                return False, None

        return True, index

    def run(self):

        candidate = {(item,): len(lines) for item, lines in self.item2line_index.items()}

        # k = 1 frequent sets
        # e.g. {1: {('1',): 5, ('3',): 7, ('4',): 5, ('6',): 4, ('2',): 6, ('5',): 3}}
        large_itemsets = {
            1: {item: count for item, count in candidate.items() if (count / self.total_line) >= self.min_support}
        }

        # 由 k-1 计算 k
        k = 2
        while large_itemsets[k - 1]:
            # join and prune 的前提是有序
            itemsets_list = sorted(item for item in large_itemsets[k - 1].keys())
            c_k = utl.gen_possible_itemset(itemsets_list)

            found_itemsets = dict()

            for candidate in c_k:
                over_min_support, indices = self.items_index(candidate)
                if over_min_support:
                    found_itemsets[candidate] = len(indices)
            large_itemsets[k] = {i: counts for (i, counts) in found_itemsets.items()}
            k += 1
        return large_itemsets


if __name__ == '__main__':
    data = "/Users/zihengzhang/KTH/ID2222-FID3016-HT22-Data-Mining/T10I4D100K.dat"
    apriori = APriori(file_path=data, min_support=0.01, min_confidence=0.5)
    res = apriori.run()

    for i in range(1, len(res) + 1):
        print("k =", i, res[i])
