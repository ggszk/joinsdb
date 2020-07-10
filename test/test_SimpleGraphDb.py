import pytest
import sys
sys.path.append('..')

from joinsdb import JoinsDb
from jdb_st_SimpleGraphDb import SimpleGraphDb

# for Neo4j connection
uri = "bolt://localhost:7687"
user = "neo4j"
passwd = "neo4jneo4j"

@pytest.mark.parametrize(('from_id', 'result', 'to_id', 'dijkstra_result', 'label'), [
    (
        0,
        [(1, 1)],
        2,
        (3, [0, 1, 2]),
        "g1"
    ),
        (
        0,
        [(2, 4), (9, 6), (1, 3)],
        8,
        (12, [0, 1, 3, 5, 8]),
        "g2"
    ),
    (
        0,
        [(2, 3), (1, 4)],
        4,
        (9, [0, 2, 3, 4]),
        "g3"
    )
])

def test_SimpleGraphDb(from_id, result, to_id, dijkstra_result, label) :
    jdb = JoinsDb()
    jdb.setStorage(SimpleGraphDb({
        'uri' : "bolt://localhost:7687",
        'user' : "neo4j",
        'passwd' :"neo4jneo4j",
        'label' : label
    }))
    assert jdb.getNextNodes(from_id) == result
    assert jdb.dijkstra(from_id, to_id) == dijkstra_result

