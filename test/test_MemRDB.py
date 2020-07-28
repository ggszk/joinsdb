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
    r1 = [(1, 2), (1, 3)]
    assert [(3,), (4,)] == rdb.call(r1, 'add')
    assert [(2,), (3,)] == rdb.call(r1, 'multiple')

    # ast execution test
    ast1 = ['select', ['project', ['list', ['id', 'col2']]], ['from', ['as', 'table3', ['id', 'table3']]]]
    ast2 = ['select', ['project', ['list', ['id', 'col2'], ['id', 'col3']]], ['from', ['as', 'table3', ['id', 'table3']]]]
    ast3 = ['select', ['project', ['list', ['id', 'col2'], ['call', 'add', ['list', ['id', 'col2'], ['id', 'col3']]]]], ['from', ['as', 'table3', ['id', 'table3']]]]
    assert [(1,), (2,)] == rdb.execute_ast({}, ast1)
    assert [(1, 2), (2, 3)] == rdb.execute_ast({}, ast2)
    assert [(1, 3), (2, 5)] == rdb.execute_ast({}, ast3)