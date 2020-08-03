# Simple multi graph database
# Neo4j + SQLite

import sys
from Neo4j import Neo4j
from SQLite import SQLite

class SimpleMultiDb:
    # initialize
    def __init__(self, param):
        if len(param) != 2 :
            print('error :parameter object must be {({SimpleGraphDb_conection_param},{SQLite_connection_param})}', file=sys.stderr)
            sys.exit(1)

        # for Neo4j connection
        self.neo4j = Neo4j({
            'uri' : param[0]['uri'],
            'user' : param[0]['user'],
            'passwd' : param[0]['passwd'],
        })
        self.label = param[0]['label']
        # for SQLite connection
        self.sqlite = SQLite(param[1]['db'])
        self.table = param[1]['table']
    
    # close
    def close(self):
        self.sqlite.close()

    # Get adjacent nodes from Neo4j
    def getNextNodes(self, node_id):
        return_ids = []
        # default label and relationship type
        label = self.label
        rel_type = "CONNECT_TO"
        cypher_str = "match (n:" + label + ")-[r:" + rel_type + \
            "]-(m:" + label + ") where n.n_id = " + str(node_id) + " return m.n_id, r.cost"
        # print(cypher_str) # for debug
        return_ids = self.neo4j.executeQuery(cypher_str)

        return return_ids

    # Get property of the node from SQLite
    def getProperty(self, node_id) :
        return_categorys =  self.sqlite.executeQuery("select category from " + self.table + " where n_id = " + str(node_id))
        return return_categorys[0][0]

    # Get nodes by specifing attribute value
    def getNode(self, value) :
        result =  self.sqlite.executeQuery("select n_id from " + self.table + " where category = " + str(value))
        result_list = []
        for r in result :
            result_list.append(r[0])
        return result_list
