"""
Authors: Chengyang Huang, Ziheng Zhang
Course:  ID2222 Data Mining
"""
import itertools
from typing import List

"""
Implement join_step and prune_step

[Fast Algorithms for Mining Association Rules](https://rakesh.agrawal-family.com/papers/vldb94apriori.pdf)

zhihu: https://www.zhihu.com/question/19912364/answer/963934469
blog: http://blog.zhengyi.one/association-rule-mining.html
"""


def join_step(items: List[tuple]):
    """
    generate k frequent set from k - 1 frequent set

    :param: items: [(1, 3), (2, 3), (2, 4), (2, 5), (3, 5)]
    :return: [(2, 3, 4), (2, 3, 5), (2, 4, 5)]]
    """
    i = 0
    items_len = len(items)
    join_step_res = []

    while i < items_len:
        ignore_item = 1

        *now_head, now_tail = items[i]  # (1, 2, 3) => head=(1, 2), tail=(3,)
        tail_items = [now_tail]

        for j in range(i + 1, len(items)):
            *next_head, next_tail = items[j]

            if now_head == next_head:
                tail_items.append(next_tail)
                ignore_item += 1
            else:
                break

        now_head_tuple = tuple(now_head)
        for a, b in sorted(itertools.combinations(tail_items, 2)):
            join_step_res.append(now_head_tuple + (a,) + (b,))

        i = i + ignore_item
    return join_step_res


def prune_step(original_items, join_step_items):
    """
    delete all itemset c in C_{k} such that some (k-1)-subset of c is NOT in L_{k-1}

    :param: original_items: [(1, 3), (2, 3), (2, 4), (2, 5), (3, 5)]
    :param: join_step_items: [(2, 3, 4), (2, 3, 5), (2, 4, 5)]
    :return: [(2, 3, 5)]
    """
    original_items = set(original_items)
    true_join_res = []
    for gen_item in join_step_items:
        existed = True

        for i in range(len(gen_item) - 1 - 1):
            removed = gen_item[:i] + gen_item[i + 1:]
            if removed not in original_items:
                existed = False
                break

        if existed:
            true_join_res.append(gen_item)
    return true_join_res


def gen_possible_itemset(items: List[tuple]):
    join_step_items = join_step(items)
    pruned_items = prune_step(original_items=items, join_step_items=join_step_items)
    return pruned_items


if __name__ == '__main__':
    test = [('1',), ('2',), ('3',), ('4',), ('5',), ('6',)]
    print(gen_possible_itemset(test))
