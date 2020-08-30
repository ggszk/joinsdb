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
    r1 = db[2]
    r2 = db[3]
    result = rdb.join(r1, r2, (0, 0), "eq")
    ret = rdb.project(result, (0, 1, 2))
    assert [(1, 2, 1)] == ret['data']
    ret = rdb.call(r1, 'add')
    assert [(3,), (5,)] == ret['data']
    ret = rdb.call(r1, 'multiple')
    assert [(2,), (6,)] == ret['data']
    r = db[2]
    ret = rdb.selection(r, ['=', ['id', 'col2'], ['lit', 1]])
    assert [(1, 2)] == ret['data']
    ret = rdb.selection(r, ['<', ['id', 'col2'], ['id', 'col3']])
    assert [(1, 2), (2, 3)] == ret['data']
    ret = rdb.selection(r, ['and', ['=', ['id', 'col2'], ['lit', 1]], ['!=', ['id', 'col2'], ['lit', 1]]])
    assert [] == ret['data']

    # ast execution test
    ast1 = ['select', ['project', ['list', ['id', 'col2']]], ['from', ['as', 'table3', ['id', 'table3']]]]
    ast2 = ['select', ['project', ['list', ['id', 'col2'], ['id', 'col3']]], ['from', ['as', 'table3', ['id', 'table3']]]]
    ast3 = ['select', ['project', ['list', ['id', 'col2'], ['call', 'add', ['list', ['id', 'col2'], ['id', 'col3']]]]], ['from', ['as', 'table3', ['id', 'table3']]]]
    ast4 = ['select', ['project', ['list', ['id', 'col2']]], ['from', ['as', 'table3', ['id', 'table3']]], ['where', ['=', ['id', 'col2'], ['lit', 1]]]]
    assert [(1,), (2,)] == rdb.execute_ast({}, ast1)
    assert [(1, 2), (2, 3)] == rdb.execute_ast({}, ast2)
    assert [(1, 3), (2, 5)] == rdb.execute_ast({}, ast3)
    assert [(1, )] == rdb.execute_ast({}, ast4)

    # partiql execution test
    q1 = "SELECT table3.col2 FROM table3 WHERE col3 = 3"
    q2 = "SELECT add(col2,col3) FROM table3"
    assert [(2,)] == rdb.executeQuery(q1)
    assert [(3,), (5,)] == rdb.executeQuery(q2)