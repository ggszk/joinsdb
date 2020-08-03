from Neo4j import Neo4j

# Very simple graphdb interface
class SimpleGraphDb:
    # initialize
    # label parameter is used in cypher query to get nodes attached the label
    def __init__(self, param):
        self.neo4j = Neo4j({
            'uri' : param['uri'],
            'user' : param['user'],
            'passwd' : param['passwd'],
        })
        self.label = param['label']

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
    # Get nodes by specifing attribute value
    def getNode(self, value) :
        # default label
        label = self.label
        cypher_str = "match (n:" + label + ") where n.category = " + str(value) + " return n.n_id"
        result = self.neo4j.executeQuery(cypher_str)
        result_list = []
        for r in result :
            result_list.append(r[0])
        return result_list

    # Get property of the node
    def getProperty(self, node_id) :
        # default label
        label = self.label
        cypher_str = "match (n:" + label + ") where n.n_id = " + str(node_id) + " return n.category"
        result = self.neo4j.executeQuery(cypher_str)
        # result will be list with one element
        return result[0][0]
