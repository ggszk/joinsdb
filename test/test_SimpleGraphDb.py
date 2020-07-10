import pytest
import sys
sys.path.append('..')

from joinsdb import JoinsDb
from jdb_st_SimpleGraphDb import SimpleGraphDb

# for Neo4j connection
uri = "bolt://localhost:7687"
user = "neo4j"
passwd = "neo4jneo4j"

@pytest.mark.parametrize(('from_id', 'result', 'to_id', 'dijkstra_result'), [
    (
        0,
        [(1, 1)],
        2,
        (3, [0, 1, 2])
    )
])

def test_SimpleGraphDb(from_id, result, to_id, dijkstra_result) :
    jdb = JoinsDb()
    jdb.setStorage(SimpleGraphDb({
        'uri' : "bolt://localhost:7687",
        'user' : "neo4j",
        'passwd' :"neo4jneo4j",
        'label' : "g1"
    }))
    assert jdb.getNextNodes(from_id) == result
    assert jdb.dijkstra(from_id, to_id) == dijkstra_result

