from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import heapq

class OSPFRoutingProtocol(DatagramProtocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.lsdb = {}
        self.neighbor_routers = []

    def startProtocol(self):
        self.transport.joinGroup("224.0.0.0")
        print(f"Started OSPF protocol on {self.host}:{self.port}")
        if self.port == 8000:
            self.sendLSA("A", {"B": 2, "C": 4, "D": 7})
    
    def sendLSA(self, router, links):
        lsa = f"{router},{','.join([f'{dest}:{cost}' for dest, cost in links.items()])}"
        self.transport.write(lsa.encode(), ("224.0.0.0", self.port))

    def datagramReceived(self, datagram, address):
        lsa = datagram.decode()
        source, links_str = lsa.split(",", 1)
        links = {link.split(":")[0]: int(link.split(":")[1]) for link in links_str.split(",")}
        self.updateLSDB(source, links)
        print(f"Received LSA from {address}: {lsa}")

    def updateLSDB(self, router, links):
        self.lsdb[router] = links
        self.calculateShortestPaths()

    def calculateShortestPaths(self):
        def dijkstra(source):
            min_heap = [(0, source)]
            distances = {router: float('inf') for router in self.lsdb}
            distances[source] = 0
            previous_nodes = {router: None for router in self.lsdb}

            while min_heap:
                current_distance, current_router = heapq.heappop(min_heap)

                if current_distance > distances[current_router]:
                    continue

                for neighbor, weight in self.lsdb.get(current_router, {}).items():
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_router
                        heapq.heappush(min_heap, (distance, neighbor))

            return distances, previous_nodes

        distances, previous_nodes = dijkstra(self.host)
        print("Routing table updated:")
        print("Destination\tNext Hop\tCost")
        for destination, cost in distances.items():
            next_hop = self.getNextHop(destination, previous_nodes)
            print(f"{destination}\t\t{next_hop}\t\t{cost}")

    def getNextHop(self, destination, previous_nodes):
        if previous_nodes[destination] is None:
            return None
        while previous_nodes[destination] != self.host:
            destination = previous_nodes[destination]
        return destination

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000

    protocol = OSPFRoutingProtocol(host, port)
    reactor.listenMulticast(port, protocol, listenMultiple=True)
    reactor.run()
