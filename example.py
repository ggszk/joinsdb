#
# Samples for using JoinsDb
#
import sys
import pprint
sys.path.append('./drivers')
from MemGraph import MemGraph
from SimpleMultiDb import SimpleMultiDb
from joinsdb import JoinsDb
from MemRDB import MemRDB

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
result = jdb.one_poi_trip(0, 8, 1)
print(result)
result = jdb.one_poi_trip2(0, 8, 1)
print(result)

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