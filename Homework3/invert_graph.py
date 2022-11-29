from centrality import DatasetIterator
from typing import Dict, Tuple, List
import os

data = "/Users/zihengzhang/KTH/ID2222-FID3016-HT22-Data-Mining/web-Google.txt"
dataIt = DatasetIterator(data)
inverted_graph:Dict[int, List[int]] = dict()

maxx = 0
for (frm, to) in dataIt:
    frm = int(frm)
    to = int(to)
    if to not in inverted_graph:
        inverted_graph[to] = []
    inverted_graph[to].append(frm)
    maxx = max(maxx, frm, to)

for k in inverted_graph.keys():
    inverted_graph[k] = sorted(inverted_graph[k])

dstFile = open("inverted_graph.txt", "w")
vis = set()
for i in range(maxx+1):
    if i not in inverted_graph:
        continue
    if i in vis:
        continue
    vis.add(i)
    for j in inverted_graph[i]:
        # to from
        dstFile.write("{} {}{}".format(i, j, os.linesep))
    for j in inverted_graph[i]:
        if j in inverted_graph and j not in vis:
            vis.add(j)
            for k in inverted_graph[j]:
                dstFile.write("{} {}{}".format(j, k, os.linesep))
