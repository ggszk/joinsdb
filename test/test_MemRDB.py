import pytest
import sys
sys.path.append('..')
sys.path.append('../drivers')
from MemRDB import MemRDB

db = {
    'table1' : {
        'meta' : ("col1", "col2"),
        'data' : [
            ('v11', 'v12'),
            ('v21', 'v22'),
            ('v31', 'v32')
        ]
    },
    'table2' : {
        'meta' : ("col2", "col3"),
        'data' : [
            ('v12', 'v13'),
            ('v22', 'v23'),
            ('v32', 'v33')
        ]
    },
    'table3' : {
        'meta' : ("col2", "col3"),
        'data' : [(1, 2), (2, 3)]
    },
    'table4' : {
        'meta' : ("col2", "col3"),
        'data' : [(1, 4), (3, 5)]
    }
}

def test_MemRDB() :
    # Relational operator test
    rdb = MemRDB(db)
    r1 = db['table3']['data']
    r2 = db['table4']['data']
    result = rdb.join(r1, r2, (0, 0), "eq")
    assert [(1, 2, 1)] == rdb.project(result, (0, 1, 2))
