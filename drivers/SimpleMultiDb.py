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
            "]->(m:" + label + ") where n.n_id = " + str(node_id) + " return m.n_id, r.cost"
        # print(cypher_str) # for debug
        return_ids = self.neo4j.executeQuery(cypher_str)

        return return_ids

    # Get property of the node from SQLite
    def getProperty(self, node_id) :
        return_interests =  self.sqlite.executeQuery("select interest from " + self.table + " where n_id = " + str(node_id))
        return return_interests[0]

    # join operator
    # r1, r2: target relations
    # index : index of join key. for example (1, 2) means key of t1 is 1, and key of t2 is 2 
    # operator : comparison operator for comparing keys: now only "eq"(=) is supported
    def join(self, r1, r2, index, operator) :
        # operator check
        if operator != "eq" :
            print('error :sorry, only equi join is supported', file=sys.stderr)
            sys.exit(1)

        # Nested loop join
        result = []
        for t1 in r1 :
            for t2 in r2 :
                if t1[index[0]] == t2[index[1]] :
                    result.append(t1 + t2)
        return result

    # projection operator
    # r: target relation
    # index : index of projected columns
    def project(self, r, index) :
        result = []
        for t in r :
            result_tuple = ()
            for idx in index :
                result_tuple = result_tuple + t[idx:idx+1]
            result.append(result_tuple)
        return result

