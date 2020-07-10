#
# JoinsDB: Integrated interface to various storage engines
#

import heapq

# Main class
class JoinsDb:
    # Change storage engine
    def setStorage(self, st) :
        self.storage = st

    # Get adjacent nodes
    def getNextNodes(self, node_id):
        return self.storage.getNextNodes(node_id)

    # Shortest path, dijkstra
    # Returns (cost, path)
    def dijkstra(self, from_id, to_id):
        # fixed cost to the node: key: node_id, value: cost
        cost = {}
        # flag to cost to the node is fixed
        fixed = {}

        # cost to the current node
        cur_cost = 0

        # tuple in priority queue: ("cost to the node", "node id", "parent of the node")
        pq = []
        heapq.heappush(pq, (0, from_id, None))

        # for route tracking
        parent = {}

        # if the priority queue is empty,  exit
        while len(pq) > 0:
            # if the cost of the to-node is fixed, break
            if fixed.get(to_id) :
                break
            cur_node_t = heapq.heappop(pq)
            # For skipping duplicating node in priority queue
            if fixed.get(cur_node_t[1]) :
                continue
            cur_cost = cur_node_t[0]
            cur_id = cur_node_t[1]
            cost[cur_id] = cur_node_t[0]
            fixed[cur_id] = True
            parent[cur_id] = cur_node_t[2]
            #print(str(cur_id) + " " +str(cur_cost)) # for debug

            n_nodes = self.getNextNodes(cur_id)
            for node in n_nodes:
                #print("\t" + str(node[0]) + " " + str(node[1]) + " " + str(cost.get(node[0]))) # for debug
                if not fixed.get(node[0]) :
                    heapq.heappush(pq, (cur_cost + node[1], node[0], cur_id))

        # not found -> return None
        route = None
        # route found
        if cost.get(to_id) is not None:
            # get route
            tmp_id = to_id
            route = [to_id]
            while tmp_id != from_id:
                route.append(parent[tmp_id])
                tmp_id = parent[tmp_id]
            route.reverse()
        return (cost.get(to_id), route)

