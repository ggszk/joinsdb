#
# Samples for using JoinsDb
#
import sys
sys.path.append('./drivers')
from MemGraph import MemGraph
from SimpleGraphDb import SimpleGraphDb
from joinsdb import JoinsDb

# adjacent list, both direction, element is (node_id, cost)
g2 = [
    [(1, 3), (9, 6), (2, 4)],
    [(3, 5), (0, 3)],
    [(0, 4), (4, 6), (7, 3)],
    [(1, 5), (5, 2), (6, 1)],
    [(2, 6)],
    [(3, 2), (8, 2)],
    [(3, 1)],
    [(2, 3)],
    [(5, 2), (9, 7)],
    [(0, 6), (8, 7)]
]

# memory storage sample
jdb = JoinsDb()
jdb.setStorage(MemGraph(g2))
result = jdb.dijkstra(0, 8)
print(result)

# neo4j storage sample
jdb.setStorage(SimpleGraphDb({
    'uri' : "bolt://localhost:7687",
    'user' : "neo4j",
    'passwd' :"neo4jneo4j",
    'label' : "g1"
}))
print(jdb.getNextNodes(0))
result = jdb.dijkstra(0, 2)
print(result)