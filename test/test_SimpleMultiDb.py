import pytest
import sys
sys.path.append('..')
sys.path.append('../drivers')
from SimpleMultiDb import SimpleMultiDb
from joinsdb import JoinsDb

def test_SimpleMultiDb() :

    # Simple multi-database sample
    smdb = SimpleMultiDb([{
            'uri' : "bolt://localhost:7687",
            'user' : "neo4j",
            'passwd' :"neo4jneo4j",
            'label' : "g2"
        },
        {
            'db' : "sample.sqlite3",
            'table' : "g2_r"
        }
    ])

    # Graph operator test
    assert [(2, 4), (9, 6), (1, 3)] == smdb.getNextNodes(0)

    smdb.close()

    # trip plannning query on simple multi database
    jdb = JoinsDb()
    jdb.setStorage(SimpleMultiDb([{
            'uri' : "bolt://localhost:7687",
            'user' : "neo4j",
            'passwd' :"neo4jneo4j",
            'label' : "g2"
        },
        {
            'db' : "sample.sqlite3",
            'table' : "g2_r"
        }
    ]))
    assert (12, [0, 1, 3, 5, 8], 3) == jdb.one_poi_trip(0, 8, 1)
    assert (12, [0, 1, 3, 5, 8], 3) == jdb.one_poi_trip2(0, 8, 1)

    jdb.close()
