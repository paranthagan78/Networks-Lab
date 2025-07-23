# from typing import Optional
from twisted.internet import reactor,protocol
from collections import deque
class echoserver(protocol.Protocol):

    def connectionMade(self):
        print('client connected')

    def dataReceived(self, data):
        recv=eval(data.decode())
        graph=recv.get('graph')
        start=recv.get('start')
        msg=recv.get('msg')
        connected=self.find_connected_edges(graph,start)
        for i in connected:
            print(f'message sent to {i} is {msg}')
        self.transport.write(f'msg sent'.encode())
        self.transport.loseConnection()
    def find_connected_edges(self,adjacency_list, source):
        
        if source not in adjacency_list:
            return []  # Source vertex not found in the adjacency list

        visited = set()
        connected_vertices = []

        def dfs(vertex):
            visited.add(vertex)
            connected_vertices.append(vertex)

            for neighbor in adjacency_list[vertex]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(source)

        return connected_vertices


class echofactory(protocol.Factory):
    def buildProtocol(self, addr):
        return echoserver()

if __name__=='__main__':
    reactor.listenTCP(8000,echofactory())
    reactor.run()