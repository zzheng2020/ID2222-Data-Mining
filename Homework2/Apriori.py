"""
Authors: Chengyang Huang, Ziheng Zhang
Course:  ID2222 Data Mining
"""

import collections
import itertools
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
        self.total_line -= 1

    def items_index(self, itemset):
        itemset = sorted(itemset, key=lambda item: len(self.item2line_index[item]), reverse=True)

        item = itemset.pop()
        index = self.item2line_index[item]
        support = len(index) / self.total_line

        # frequent set 中的元素必须每个都满足要求
        if support < self.min_support:
            return False, None, support

        while itemset:
            item = itemset.pop()

            # 两个元素共同出现在了哪些行, 并且判断是否满足要求
            index = index.intersection(self.item2line_index[item])
            support = len(index) / self.total_line
            if support < self.min_support:
                return False, None, support

        return True, index, support

    def gen_rules(self, frequent_items: tuple):
        """
        先得到 k-frequent-set, 然后生成 rules.
        
        (代码写的比较丑 :D, 感觉写的是对的, 不确定...🫤)
        (时间复杂度貌似是 O(n^2) 的, n 是 k-frequent-set 的大小, 但 k-frequent-set 本身就不大, 所以跑起来不是很慢...)
        (如果写错了, 就直接删了吧 🥹)

        e.g. rule: lhs => rhs
        lhs: left hand side, 表示规则左边的部分
        rhs: right hand side, 表示规则右边的部分

        用 bfs 去搜有哪些规则 >= min_confidence

        首先枚举 rhs 大小为 1 的时候, 比如 3-frequent-set = {1, 2, 3}, 那么可以枚举出规则 (1, 2) => (3), (1, 3) => (2), etc.
        有了 rhs 之后, lhs 就是整个集合减去 rhs.

        然后计算这个规则的 confidence, 如果 confidence >= min_confidence 就加入到队列, 否则不满足要求.
        如果某一个规则不满足要求, 比如 (1, 2) => (3) 不满足要求, 那么右边包含 (3) 的规则都不满足要求.
        因为 confidence[(1, 2) => (3)] = P(1, 2, 3) / P(1, 2), 显然 P(1) >= P(1, 2), P(2) >= P(1, 2),
        那么如果 P(1, 2) 作为分母不能让式子满足要求, 那么分子不变的情况下, 分母变大了, 显示式子也不会满足要求.

        然后将队列的每一个元素拿出来进行计算, 生成规则, 判断是否满足要求.

        当队列中的元素的 lhs 大小为 1 时, 说明搜到了树的叶子结点, 那么输出答案.

        只保留叶子结点的原因是, 比如规则 (1) => (2, 3) 满足要求, 那么 (1, 2) => (3), (1, 3) => (2) 都会满足要求,
        所以就只保留了叶子结点的规则.

        res 中存的是结果,
        e.g. [{('704',): ('825', '39')}, {('39',): ('704', '825')}, {('825',): ('704', '39')}] 表示
        规则 (704) => (825, 39), (39) => (704, 825), (825) => (704. 39).

        """
        que = collections.deque()

        lhs_tuples = frequent_items

        ignored = tuple()

        for items in itertools.combinations(frequent_items, 1):
            rhs_set = set(items)
            lhs_set = set(lhs_tuples) - rhs_set
            
            _, _, rhs_support = self.items_index(tuple(rhs_set))
            _, _, lhs_rhs_union_support = self.items_index(tuple(lhs_set.union(rhs_set)))

            if rhs_support > 0:
                confidence = lhs_rhs_union_support / rhs_support
            else:
                confidence = 0

            if confidence >= self.min_confidence:
                que.append({tuple(lhs_set): tuple(rhs_set)})
            else:
                ignored += (tuple(rhs_set))
            
        ignored = set(ignored)
        

        # 不重复搜搜过的规则
        has_appeared = collections.defaultdict(int)
        while len(que) > 0:
            head_dic: dict = que.popleft()
            
            if len(head_dic) == 0:
                continue

            lhs_tuples = list(head_dic.keys())[0]
            rhs_tuples = list(head_dic.values())[0]

            if len(lhs_tuples) == 1:
                # 不熟悉 python ...😅, 因为 popleft 把元素拿出来了, 现在又要放回去 😅
                que.append(head_dic)
                break

            for items in itertools.combinations(lhs_tuples, 1):
                rhs = rhs_tuples + items
                
                rhs_set = set(rhs)
                if len(rhs_set.intersection(ignored)) > 0:
                    continue

                if has_appeared[tuple(sorted(rhs))] > 0:
                    continue
                else:
                    has_appeared[tuple(sorted(rhs))] += 1

                lhs_set = set(lhs_tuples) - set(items)

                que.append({tuple(lhs_set): tuple(rhs_set)})
            
            # print("---")
        
        res = []
        while len(que) > 0:
            head_dic = que.popleft()
            lhs_tuples = list(head_dic.keys())[0]
            rhs_tuples = list(head_dic.values())[0]
            res.append({tuple(lhs_tuples): tuple(rhs_tuples)})
        
        return res        

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
                # print("candidate:", candidate)
                over_min_support, indices, _ = self.items_index(candidate)
                if over_min_support:
                    found_itemsets[candidate] = len(indices)
            large_itemsets[k] = {i: counts for (i, counts) in found_itemsets.items()}
            k += 1
        return large_itemsets


if __name__ == '__main__':
    data = "/Users/zihengzhang/KTH/ID2222-FID3016-HT22-Data-Mining/T10I4D100K.dat" # min_support = 0.01
    apriori = APriori(file_path=data, min_support=0.01, min_confidence=0.10)

    res = apriori.run()

    for i in range(1, len(res) + 1):
        print("k =", i, list(res[i].keys()))
        for item in list(res[i].keys()):
            rules = apriori.gen_rules(item)
            if len(rules) == 0:
                continue
            else:
                print("rules:", rules)

"""
1 3 4 6
2 3 4
1 2 3
2 6
2 3 4 5
2 3 5
1 2 3 4 6
1 3 4 5 6
1
"""