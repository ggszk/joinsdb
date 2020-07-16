#
# Samples for using JoinsDb
#
import sys
import pprint
sys.path.append('./drivers')
from Neo4j import Neo4j
from MemGraph import MemGraph
from SimpleGraphDb import SimpleGraphDb
from SQLite import SQLite
from SimpleMultiDb import SimpleMultiDb
from joinsdb import JoinsDb

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

# insert interest information to adjacent list of graph
def insert_poi(g, poi) :
    result = []
    for n in g2 :
        record = []
        for e in n :
            record.append((e[0], e[1], poi[e[1]]))
        result.append(record)
    return result

g2_poi = insert_poi(g2, interest)

# on memory graph storage sample
jdb = JoinsDb()
jdb.setStorage(MemGraph(g2))
result = jdb.dijkstra(0, 8)
print(result)

# trip planning query (one poi) sample
jdb.setStorage(MemGraph(g2_poi))
result = jdb.one_poi_trip(0, 8, 1)
print(result)

# neo4j storage sample
jdb.setStorage(Neo4j({
    'uri' : "bolt://localhost:7687",
    'user' : "neo4j",
    'passwd' :"neo4jneo4j",
}))
# Pass through cypher query
result = jdb.executeQuery("match (n:g1) return n")
print(result)

# simple graph storage sample
jdb.setStorage(SimpleGraphDb({
    'uri' : "bolt://localhost:7687",
    'user' : "neo4j",
    'passwd' :"neo4jneo4j",
    'label' : "g1"
}))
print(jdb.getNextNodes(0))
result = jdb.dijkstra(0, 2)
print(result)

# trip planning query on Neo4j
jdb.setStorage(SimpleGraphDb({
    'uri' : "bolt://localhost:7687",
    'user' : "neo4j",
    'passwd' :"neo4jneo4j",
    'label' : "g2"
}))
result = jdb.one_poi_trip(0, 8, 1)
print(result)

# SQLite sample
jdb.setStorage(SQLite("test/sample.sqlite3"))
result = jdb.executeQuery("select * from g2_r")
jdb.close()
print(result)

# Simple multi-database sample
smdb = SimpleMultiDb([{
        'uri' : "bolt://localhost:7687",
        'user' : "neo4j",
        'passwd' :"neo4jneo4j",
        'label' : "g2"
    },
    {
        'db' : "test/sample.sqlite3",
        'table' : "g2_r"
    }
])
r1 = [(1, 2), (2, 3)]
r2 = [(1, 4), (3, 5)]
result = smdb.join(r1, r2, (0, 0), "eq")
result2 = smdb.project(result, (0, 1, 2))
pprint.pprint(result2, width=50)

result3 = smdb.getNextNodes(0)
print(result3)
smdb.close()

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



