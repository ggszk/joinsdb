#
# Samples for using JoinsDb
#
import sys
import pprint
sys.path.append('./drivers')
from MemGraph import MemGraph
from SimpleMultiDb import SimpleMultiDb
from SimpleGraphDb import SimpleGraphDb
from joinsdb import JoinsDb
from MemRDB import MemRDB
from VirtualDB import VirtualDB
from PartiQL import PartiQL

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

# if poi -> 1, else -> 0
interest = [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]

# trip planning query (one poi) sample
# on memory graph storage sample
jdb = JoinsDb()
jdb.setStorage(MemGraph(g2))
jdb.setProperty(interest)
result = jdb.one_poi_trip(0, 8, 1)
print(result)
result = jdb.one_poi_trip2(0, 8, 1)
print(result)

jdb.setStorage(SimpleGraphDb({
        'uri' : "bolt://localhost:7687",
        'user' : "neo4j",
        'passwd' :"neo4jneo4j",
        'label' : "g2"
    }
))
result = jdb.one_poi_trip(0, 8, 1)
print(result)

# trip plannning query on simple multi database
jdb.setStorage(SimpleMultiDb([{
        'uri' : "bolt://localhost:7687",
        'user' : "neo4j",
        'passwd' :"neo4jneo4j",
        'label' : "g2"
    },
    {
        'db' : "test/sample.sqlite3",
        'table' : "g2_r"
    }
]))
#result = jdb.one_poi_trip(0, 8, 1)
#print(result)
#result = jdb.one_poi_trip2(0, 8, 1)
#print(result)

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
query = [
    "SELECT table3.col2, col3 FROM table3",
    "SELECT add(col2,col3) FROM table3"
]
jdb.setStorage(MemRDB(db))
for q in query :
    print(jdb.executeQuery(q))

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
        }
    ],
    # metadata for enriching database semantics
    'metadata' : {
        # relationships
        # functions
    }
}

# Virtual DB
vdb = VirtualDB(param)
print(vdb.executeQuery("SELECT table3.col2, col3 FROM table3"))

# PartiQL DB
db = {
    'hr': {
        'employees': [
            { 'id': 3, 'name': 'Bob_Smith',   'title': None }, 
            { 'id': 4, 'name': 'Susan_Smith', 'title': 'Dev Mgr' },
            { 'id': 6, 'name': 'Jane_Smith',  'title': 'Software Eng 2'}
        ]
    }
}

pdb = PartiQL(db)
print(pdb.get_relation(db, 'hr'))
r = db['hr']['employees']
print(pdb.project(r, ['name', 'title']))
print(pdb.selection(r, ['=', ['id', 'id'], ['lit', 4]]))
print(pdb.executeQuery("SELECT name FROM employees"))
print(pdb.executeQuery("SELECT id FROM employees WHERE id = 3"))
print(pdb.executeQuery("SELECT name FROM employees WHERE name = 'Bob_Smith'"))
