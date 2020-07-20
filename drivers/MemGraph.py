# On memory graph
class MemGraph:
    # initialize
    def __init__(self, param):
        # param: adjacent map of the graph
        self.adj_map = param
        self.property = []
 
    # Graph construction
    def add_node(self):
        self.adj_map.append([])

    def add_edge(self, from_id, to_id, cost):
        self.adj_map[from_id].append((to_id, cost))
    
    def setProperty(self, property) :
        if len(self.adj_map) < len(property) :
            print('error :property list length must be less than node list size', file=sys.stderr)
            sys.exit(1)
        else :
            self.property = property

    # Get adjacent nodes
    def getNextNodes(self, node_id):
        return self.adj_map[node_id]

    # Get property of the node
    def getProperty(self, node_id) :
        return self.property[node_id]

    # Get node by specifing property value
    def getNode(self, value) :
        # find node ids
        result = []
        i = 0
        for p in self.property :
            if p == value :
                result.append(i)
            i = i + 1
        return result