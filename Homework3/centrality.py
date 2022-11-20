from cardinality import HyperLogLogCounter
from typing import Dict, Tuple, List
from collections import defaultdict
import os

# assume possible to put all vertices in memory
prob_card_counter: Dict[str, HyperLogLogCounter] = dict()
# (node, iter) -> cardinality
stat: Dict[Tuple[str, int], int] = dict()


class DatasetIterator:
    def __init__(self, f):
        self.f = f

    def __iter__(self):
        self.fd = open(self.f, "r")
        return self

    def __del__(self):
        self.fd.close()

    def __next__(self):
        while True:
            line = self.fd.readline()
            if len(line) == 0:
                raise StopIteration
            if line.startswith("#"):
                continue
            data = line.strip().split()
            return (data[0], data[1])


def checkpoint(stat, round):
    with open("stat.txt", "a") as f:
        for k in prob_card_counter.keys():
            f.write("{} {} {}{}".format(k, round, str(stat[(k, round)]), os.linesep))
        f.write("====" + os.linesep)


# centrality -> distance to node
if __name__ == "__main__":
    dataIt = DatasetIterator("inverted_graph.txt")
    last = None
    cnt = 0

    # initialize probablistic counters
    for (to, frm) in dataIt:
        if to not in prob_card_counter:
            prob_card_counter[to] = HyperLogLogCounter()
            prob_card_counter[to].add(to)
            stat[(to, 0)] = 1
            stat[(to, 1)] = 0
        if frm not in prob_card_counter:
            prob_card_counter[frm] = HyperLogLogCounter()
            prob_card_counter[frm].add(frm)
            stat[(frm, 0)] = 1
            stat[(frm, 1)] = 0
        if to != last:
            if last is not None:
                stat[(last, 0)] = 1
                stat[(last, 1)] = cnt
            last = to
            cnt = 1
        else:
            cnt += 1
        prob_card_counter[to].add(frm)

    if last is not None:
        stat[(last, 0)] = 1
        stat[(last, 1)] = cnt

    checkpoint(stat, 0)
    checkpoint(stat, 1)

    round = 2
    while True:
        print("round: ", round)

        dataIt = DatasetIterator("inverted_graph.txt")
        tmpProbCardCounter: Dict[str, HyperLogLogCounter] = dict()
        last = None
        for (to, frm) in dataIt:
            if to not in tmpProbCardCounter:
                tmpProbCardCounter[to] = prob_card_counter[to]
            if frm not in tmpProbCardCounter:
                tmpProbCardCounter[frm] = prob_card_counter[frm]
            tmpProbCardCounter[to] = tmpProbCardCounter[to].union(prob_card_counter[frm])

        changed = False
        delta = 0.0

        # update probablistic counters
        for k in prob_card_counter.keys():
            prob_card_counter[k] = tmpProbCardCounter[k]
            stat[(k, round)] = prob_card_counter[k].cardinality()
            delta += stat[(k, round)] - stat[(k, round - 1)]
            if stat[(k, round)] != stat[(k, round - 1)]:
                changed = True

        print("delta: ", delta)

        checkpoint(stat, round)

        # if not changed:
        if not changed or round > 10:
            break

        round += 1

    print()
    print("calculating harmonic centrality")
    harmonic_centrality: Dict[str, float] = defaultdict(int)
    node_num = len(prob_card_counter)
    # print("node num: ", node_num)
    for i in range(1, round + 1):
        for node in prob_card_counter.keys():
            harmonic_centrality[node] += stat[(node, round)] / round

    srtd_centrality = sorted(list(map(lambda x: (x[1], x[0]), harmonic_centrality.items())), reverse=True)

    topN = 5
    print("===== top {}: {}".format(topN, srtd_centrality[:5]))
    for (v, k) in srtd_centrality[:topN]:
        print("node: {}".format(k))
        for rnd in range(1, round + 1):
            print("    round: {} cardinality: {}".format(rnd, stat[(k, rnd)]))

    bottomN = 5
    print("===== bottom {}: {}".format(bottomN, srtd_centrality[-5:]))
    for (v, k) in srtd_centrality[-bottomN:]:
        print("node: {}".format(k))
        for rnd in range(1, round + 1):
            print("    round: {} cardinality: {}".format(rnd, stat[(k, rnd)]))
