#
# JoinsDB: Integrated interface to various storage engines
#

import heapq

# Main class
class JoinsDb:
    # Change storage engine
    def setStorage(self, st) :
        self.storage = st

    # Pass through query execution
    def executeQuery(self, query) :
        return self.storage.executeQuery(query)
    
    # Close connection
    def close(self) :
        self.storage.close()
    
    # Get adjacent nodes
    def getNextNodes(self, node_id):
        return self.storage.getNextNodes(node_id)

    # Get node by specifing attribute value
    def getNode(self, value) :
        return self.storage.getNode(value)
    
    # Set property values of all nodes at once (for only MemGraph)
    def setProperty(self, p) :
        self.storage.setProperty(p)
    
    # Get property of the node
    def getProperty(self, node_id) :
        return self.storage.getProperty(node_id)

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
    
    # Simple trip planning query using bidirectional dijkstra
    # Shortest path through one point of interest
    # Returns (cost, path, id of poi)
    def one_poi_trip(self, from_id, to_id, interest) :
        # fixed cost to the node: key: node_id, value: cost
        cost_f = {}
        cost_t = {}
        total_cost = 100000 # infinity

        # flag to cost to the node is fixed
        fixed_f = {}
        fixed_t = {}

        # cost to the current node
        cur_cost_f = 0
        cur_cost_t = 0

        # tuple in priority queue: ("cost to the node", "node id", "parent of the node", "category(interest)")
        pq_f = []
        pq_t = []
        heapq.heappush(pq_f, (0, from_id, None, self.getProperty(from_id)))
        heapq.heappush(pq_t, (0, to_id, None, self.getProperty(to_id)))

        # for route tracking
        parent_f = {}
        parent_t = {}

        # result : (cost, path, id_of_poi)
        result = ()
        poi_id = None

        # Minumum distance of 'from or to'-node to poi : for decision to stop
        # If POI not found, this value is current node's cost
        poi_min_cost_f = 0
        poi_min_found_f = False
        poi_min_cost_t = 0
        poi_min_found_t = False

        # Path finding
        while(True) :
            # if one queue is empty, no route exit
            if len(pq_f) == 0 or len(pq_t) == 0 :
                result = (None, [], None)
                break
            # exit when cannot find shorter path (triangle inequality)
			# (total cost) < (current f-side cost) + (minum t-side poi cost); for both side
            if (cur_cost_f + poi_min_cost_t > total_cost) and (poi_min_cost_f + cur_cost_t > total_cost) :
                # get route : from -> poi
                tmp_id = poi_id
                route_f = [poi_id]
                while tmp_id != from_id:
                    route_f.append(parent_f[tmp_id])
                    tmp_id = parent_f[tmp_id]
                route_f.reverse()
                # get route : poi -> to 
                tmp_id = poi_id
                route_t = [poi_id]
                while tmp_id != to_id:
                    route_t.append(parent_t[tmp_id])
                    tmp_id = parent_t[tmp_id]
                # delete poi for avoiding duplicate
                route_t.pop(0)
                result = (total_cost, route_f + route_t, poi_id)
                break
            # expand from-side : compare cost of top of the queues
            if pq_f[0][0] < pq_t[0][0] :
                cur_node_f_t = heapq.heappop(pq_f)
                # For skipping duplicating node in priority queue
                if fixed_f.get(cur_node_f_t[1]) :
                    continue
                #  If POI is found, check total path
                if cur_node_f_t[3] == interest :
                    if not poi_min_found_f :
                        poi_min_cost_f = cur_node_f_t[0]
                        poi_min_found_f = True
                    # if find the POI node in the other side, put into temp result
                    if fixed_t.get(cur_node_f_t[1]) :
                        poi_id = cur_node_f_t[1]
                        total_cost = cur_node_f_t[0] + cost_t[poi_id]
                cur_cost_f = cur_node_f_t[0]
                if not poi_min_found_f :
                    poi_min_cost_f = cur_cost_f
                cur_id_f = cur_node_f_t[1]
                fixed_f[cur_id_f] = True
                cost_f[cur_id_f] = cur_node_f_t[0]
                parent_f[cur_id_f] = cur_node_f_t[2]
                # expand next nodes
                n_nodes_f = self.getNextNodes(cur_id_f)
                for node in n_nodes_f:
                    #print("f: \t" + str(node[0]) + " " + str(node[1]) + " " + str(cost_f.get(node[0]))) # for debug
                    if not fixed_f.get(node[0]) :
                        # set (cost, node, parent, interest)
                        heapq.heappush(pq_f, (cur_cost_f + node[1], node[0], cur_id_f, self.getProperty(node[0])))

            # expand to-side : compare cost of top of the queues
            else :
                cur_node_t_t = heapq.heappop(pq_t)
                # For skipping duplicating node in priority queue
                if fixed_t.get(cur_node_t_t[1]) :
                    continue
                #  If POI is found, check total path
                if cur_node_t_t[3] == interest :
                    if not poi_min_found_t :
                        poi_min_cost_t = cur_node_t_t[0]
                        poi_min_found_t = True
                    # print("t: poi: " + str(cur_node_t_t[1])) # for debug
                    # if find the POI node in the other side, put into temp result
                    if fixed_f.get(cur_node_t_t[1]) :
                        poi_id = cur_node_t_t[1]
                        total_cost = cur_node_t_t[0] + cost_f[poi_id]
                cur_cost_t = cur_node_t_t[0]
                if not poi_min_found_t :
                    poi_min_cost_t = cur_cost_t
                cur_id_t = cur_node_t_t[1]
                fixed_t[cur_id_t] = True
                cost_t[cur_id_t] = cur_node_t_t[0]
                parent_t[cur_id_t] = cur_node_t_t[2]
                # expand next nodes
                n_nodes_t = self.getNextNodes(cur_id_t)
                for node in n_nodes_t:
                    #print("t: \t" + str(node[0]) + " " + str(node[1]) + " " + str(cost_t.get(node[0]))) # for debug
                    if not fixed_t.get(node[0]) :
                        # set (cost, node, parent, interest)
                        heapq.heappush(pq_t, (cur_cost_t + node[1], node[0], cur_id_t, self.getProperty(node[0])))
               
        return result

    # Shortest path through one point of interest
    # another method : find pois first
    # Returns (cost, path, id of poi)
    def one_poi_trip2(self, from_id, to_id, interest) :
        # find pois
        pois =  self.getNode(interest)

        # find path between poi and from- or to-node
        paths = []
        for poi in pois :
            # find from-poi path
            from_path = self.dijkstra(from_id, poi)
            # find poi-to path
            to_path = self.dijkstra(poi, to_id)
            # concatenate two paths
            paths.append(self.cat_path(from_path, to_path) + (poi,))
        # sort results and find the shortest

        return self.orderby(paths, 0)[0]

    # concatenate two paths (result of digkstra: (cost, path))
    def cat_path(self, path1, path2) :
        return (path1[0] + path2[0], path1[1][:-1] + path2[1])

    # sort result
    # index must be integer (= multi column sort is not supported)
    def orderby(self, r, index) :
        result = sorted(r, key=lambda x: x[index])
        return result