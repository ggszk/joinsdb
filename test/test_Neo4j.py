import pytest
import sys
sys.path.append('..')
sys.path.append('../drivers')

from joinsdb import JoinsDb
from Neo4j import Neo4j

def test_Neo4j() :
    # neo4j storage sample
    jdb = JoinsDb()
    jdb.setStorage(Neo4j({
        'uri' : "bolt://localhost:7687",
        'user' : "neo4j",
        'passwd' :"neo4jneo4j",
    }))
    # Pass through cypher query
    assert [({'n_id': 0},), ({'n_id': 1},), ({'n_id': 2},)] == jdb.executeQuery("match (n:g1) return n")
