# HomeWork 3 Report

**By Chengyang Huang, Ziheng Zhang, Group 25**

## Implementation

We implemented two probabilistic cardinality counter. One based on the Flajolet-Martin algorithm, the other one is based on the HyperLogLog algorithm.
We used these two counter to estimate the unique number of nodes in [Google Web Graph](https://snap.stanford.edu/data/web-Google.html), and we got similar result than the reported number.

With HyperLogLog algorithm, our estimation is `740397.7946229508`, with the Flajolet-Martin algorithm, our result is `1355607`.
Note the result might vary and the value reported above is from one run. The reported value from the dataset is `875713`.

As a second part, we chose [In-Core Computation of Geometric Centralities with HyperBall: A Hundred Billion Nodes and Beyond](https://arxiv.org/pdf/1308.2144v2.pdf) to implement.
We followed the procedure of the described algorithm, first flip the graph, then calculate the HyperBall iteratively. Using these HyperBall values as an intermediate value, we reported the nodes with top 5 and bottom 5 harmonic centrality.   
In one run, the top 3 nodes are `209190 149580 805257`, and there are many nodes whose centrality is similarly low, we reported three of them, which are `241565 621749 72500`  

## Optional Task

1. What were the challenges you faced when implementing the algorithm?

Bugs are hard to be found when implementing probabilistic counters, since the result might vary and intermediate steps are hard to trace. 

2. Can the algorithm be easily parallelized? If yes, how? If not, why? Explain.

No, the problem mostly lies in merging the result.

To do this in parallel, some algorithm must be needed to split the graph into several parts and these parts can run this algorithm alone. We didn't figure out a good way to merge the result between graph parts while getting correct HyperBall estimate.

3. Does the algorithm work for unbounded graph streams? Explain.

No, it is an iterative algorithm, the initial state requires the data from entire graph, which does not fit well with stream processing.

4. Does the algorithm support edge deletions? If not, what modification would it need? Explain.

No, when we delete an edge, all the graph needed to be computed again.