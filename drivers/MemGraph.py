# On memory graph
class MemGraph:
    # initialize
    def __init__(self, param):
        # param: adjacent map of the graph
        self.adj_map = param
 
    # Graph construction
    def add_node(self):
        self.adj_map.append([])

    def add_edge(self, from_id, to_id, cost):
        self.adj_map[from_id].append((to_id, cost))

    # Get adjacent nodes
    def getNextNodes(self, node_id):
        return self.adj_map[node_id]

     # Get node by specifing attribute value
    def getNode(self, value) :
        # extracting attribute value from adj map
        attribute = {}
        for n in self.adj_map :
            for e in n :
                attribute[e[0]] = e[2]
        # find node ids
        result = []
        for key in attribute :
            if attribute[key] == value :
                result.append(key)
        return result