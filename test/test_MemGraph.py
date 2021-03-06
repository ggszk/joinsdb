import pytest
import sys
sys.path.append('..')
sys.path.append('../drivers')

from joinsdb import JoinsDb
from MemGraph import MemGraph

# sample
# adjacent list, both direction, element is (node_id, cost)
g1 = [
    [(1, 1)],
    [(2, 2), (0, 1)],
    [(1, 2)]
]

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

g3 = [
    [(1, 4), (2, 3)],
    [(0, 4), (3, 3)],
    [(0, 3), (3, 2)],
    [(1, 3), (2, 2), (4, 4)],
    [(4, 4)]
]

# if poi -> 1, else -> 0
interest = [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]

@pytest.mark.parametrize(('graph', 'from_id', 'to_id', 'result'), [
    (
        g1,
        0,
        2,
        (3, [0, 1, 2])
    ),
    (
        g2,
        0,
        8,
        (12, [0, 1, 3, 5, 8])
    ),
    (
        g3,
        0,
        4,
        (9, [0, 2, 3, 4])
    )
])

def test_MemGraph(graph, from_id, to_id, result) :
    jdb = JoinsDb()
    jdb.setStorage(MemGraph(graph))
    assert jdb.dijkstra(from_id, to_id) == result

# trip planning query (one poi) sample
def test_tpq() :
    jdb = JoinsDb()
    jdb.setStorage(MemGraph(g2))
    jdb.setProperty(interest)
    assert (12, [0, 1, 3, 5, 8], 3) == jdb.one_poi_trip(0, 8, 1)
    assert (12, [0, 1, 3, 5, 8], 3) == jdb.one_poi_trip2(0, 8, 1)
