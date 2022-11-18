# HomeWork 2 Report

**By Chengyang Huang, Ziheng Zhang, Group 25**



## Functions

* `join_step` function

  Input: k frequent set

  Output: k + 1 frequent set

  Note: The pre-requirment is the input set is ordered.

  The logic behind this function is that if two k frequent set can generate k + 1 frequset, both of them must share the same k - 1 items.

  For example, the input k frequent set is `[(1, 2, 3), (1, 2, 4), (1, 2, 7) (1, 3, 4), (1, 3, 5), (2, 3, 4)]`, if we are at `(1, 2, 3)` now, we will consider `(1, 2, 4)` and  ` (1, 2, 4)`, but not `(1, 3, 5)`.

* `prune_step` function

  Input: `join_step` result

  Output: delete the k + 1 set whose subset does not contain k frequent set.

  The logic behind it is that if the k + 1 set if the frequent set, the subset of k + 1 set must be the k frequent set.

  For example, the `join_step` result is `[(2, 3, 4), (2, 3, 5), (2, 4, 5)]`. When we are at `(2, 3, 4)`, `prune_step` will check subset `(3, 4)` and `(2, 4)` since `(2, 3)` must be the subset of k frequent set.

* `Apriori` class

  1. Inverted index

     `item2line_index[value] = tuple(1, 2, 3...)` stores the `value` appears in the line 1, 2, 3… It allowes us to fastly calculate which rows the two elements appear in together.

  2. `large_itemsets`

     It is used to store the k frequent set.

     For example, `{1: {('1',): 5, ('3',): 7, ('4',): 5, ('6',): 4, ('2',): 6, ('5',): 3}}` means k = 1 frequent set containing 1, 3, 4, 6, 2, 5 and the following number denotes how many lines it appears in the dataset.

  3. `item_index`

     It is used to check whether the itemset meets the `min_support` requirement.

  4. `run`

     It is used to calculate frequent itemsets.

  5. `gen_rules`

     After `run`, Use BFS to generate rules. see follwing fig.

     ![conf_pruned](/Users/zihengzhang/KTH/ID2222-FID3016-HT22-Data-Mining/ID2222-Data-Mining/Homework2/pic/conf_pruned.png)

  ## Results

  ![result](/Users/zihengzhang/KTH/ID2222-FID3016-HT22-Data-Mining/ID2222-Data-Mining/Homework2/pic/result.png)