import pytest
import sys
import pprint
sys.path.append('..')
sys.path.append('../drivers')
from VirtualDB import VirtualDB

# Virtual DB
# Simple RDB on memory
db = [
    {
        'name' : 'table3',
        'meta' : ("col2", "col3"),
        'data' : [(1, 2), (2, 3)]
    },
    {
        'name' : 'table4',
        'meta' : ("col2", "col3"),
        'data' : [(1, 4), (3, 5)]
    }
]

param = {
    # database connection information 
    'db' : [
        {
            'name' : 'db1',
            'type' : 'MemRDB',
            'table' : [
                # name : virtual table name to access
                # local_name : real table name in local database
                {'name' : 'table3', 'local_name' : 'table3'},
                {'name' : 'table4', 'local_name' : 'table4'}
            ],
            # db connection information
            # MemRDB : database data
            'connect' : db
        },
        {
            'name' : 'db2',
            'type' : 'Neo4j',
            'table' : [
                # name : virtual table name to access
                # local_name : real table name in local database
                {'name' : 'g1', 'local_name' : 'g1'},
                {'name' : 'g2', 'local_name' : 'g2'},
                {'name' : 'g3', 'local_name' : 'g3'}
            ],
            # db connection information (for Neo4j)
            'connect' : {
                'uri' : "bolt://localhost:7687",
                'user' : "neo4j",
                'passwd' :"neo4jneo4j",
            }
        }
    ],
    # metadata for enriching database semantics
    'metadata' : {
        # relationships
        # functions
    }
}

@pytest.mark.parametrize(('q', 'result'), [
    (
        "SELECT table3.col2, col3 FROM table3",
        [(1, 2), (2, 3)]
    ),
        (
        "SELECT g2.n_id, g2.category FROM g2",
        [(0, 0), (1, 0), (6, 0), (2, 0), (3, 1), (4, 0), (5, 0), (7, 0), (8, 0), (9, 1)]
    ),
    (
        "SELECT g2 FROM g2",
        [({'category': 0, 'n_id': 0},), ({'category': 0, 'n_id': 1},), ({'category': 0, 'n_id': 6},), ({'category': 0, 'n_id': 2},), ({'category': 1, 'n_id': 3},), ({'category': 0, 'n_id': 4},), ({'category': 0, 'n_id': 5},), ({'category': 0, 'n_id': 7},), ({'category': 0, 'n_id': 8},), ({'category': 1, 'n_id': 9},)]
    )
])

def test_VirtualDb(q, result) :
    vdb = VirtualDB(param)
    assert result == vdb.executeQuery(q)
