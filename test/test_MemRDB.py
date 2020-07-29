import pytest
import sys
sys.path.append('..')
sys.path.append('../drivers')
from MemRDB import MemRDB

db = [
    {
        'name' : 'table1',
        'meta' : ("col1", "col2"),
        'data' : [
            ('v11', 'v12'),
            ('v21', 'v22'),
            ('v31', 'v32')
        ]
    },
    {
        'name' : 'table2',
        'meta' : ("col2", "col3"),
        'data' : [
            ('v12', 'v13'),
            ('v22', 'v23'),
            ('v32', 'v33')
        ]
    },
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

def test_MemRDB() :
    # Relational operator test
    rdb = MemRDB(db)
    r1 = db[2]['data']
    r2 = db[3]['data']
    result = rdb.join(r1, r2, (0, 0), "eq")
    assert [(1, 2, 1)] == rdb.project(result, (0, 1, 2))
    assert [(3,), (5,)] == rdb.call(r1, 'add')
    assert [(2,), (6,)] == rdb.call(r1, 'multiple')
    r = db[2]
    assert [(1, 2)] == rdb.selection(r, ['=', ['id', 'col2'], ['lit', 1]])
    assert [(1, 2), (2, 3)] == rdb.selection(r, ['<', ['id', 'col2'], ['id', 'col3']])
    assert [] == rdb.selection(r, ['and', ['=', ['id', 'col2'], ['lit', 1]], ['!=', ['id', 'col2'], ['lit', 1]]])

    # ast execution test
    ast1 = ['select', ['project', ['list', ['id', 'col2']]], ['from', ['as', 'table3', ['id', 'table3']]]]
    ast2 = ['select', ['project', ['list', ['id', 'col2'], ['id', 'col3']]], ['from', ['as', 'table3', ['id', 'table3']]]]
    ast3 = ['select', ['project', ['list', ['id', 'col2'], ['call', 'add', ['list', ['id', 'col2'], ['id', 'col3']]]]], ['from', ['as', 'table3', ['id', 'table3']]]]
    assert [(1,), (2,)] == rdb.execute_ast({}, ast1)
    assert [(1, 2), (2, 3)] == rdb.execute_ast({}, ast2)
    assert [(1, 3), (2, 5)] == rdb.execute_ast({}, ast3)