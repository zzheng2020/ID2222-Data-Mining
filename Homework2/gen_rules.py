import collections
import itertools

def gen_rules(frequent_items: tuple):
    que = collections.deque()

    lhs_tuples = frequent_items

    for items in itertools.combinations(frequent_items, 1):
        rhs_set = set(items)
        lhs_set = set(lhs_tuples) - rhs_set
        for a in rhs_set:
            print(a)
        pass
        
    
    pass


    while len(que) > 0:
        head_dic: dict = que.popleft()

        lhs_tuples = list(head_dic.keys())[0]
        rhs_tuples = list(head_dic.values())[0]

        # antecedent_len = len(lhs_tuples) - 1
        # consequent_len = len(rhs_tuples) + 1

        for items in itertools.combinations(lhs_tuples, 1):
            rhs = set(rhs_tuples)
            print(rhs)

        break

if __name__ == '__main__':
    candidates = ('a', 'b', 'c', 'd')
    gen_rules(candidates)