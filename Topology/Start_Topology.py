from twisted.internet import protocol, reactor

class StarProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory  # factory that stores all the clients connected to the server
        self.name = None  # name of the client that will connect to the server

    def connectionMade(self):
        '''establishing a connection to the server'''
        print('New client connected: ', self.transport.getPeer())
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Client disconnected")
        self.factory.removeClient(self)

    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
            print(self.name, ' has connected to the server.')
        else:
            if message.startswith('@'):
                recipient, private_message = message[1:].split(":", 1)
                self.sendthroughServer(recipient, private_message)
            else:
                self.transport.write(message.encode())

    def sendthroughServer(self, recipient, message):
        self.transport.write('message sending.....'.encode())
        self.sendPrivateMessage(recipient, message)

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recipient} not found.\n".encode())

class StarFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return StarProtocol(self)

    def removeClient(self, client):
        self.clients.remove(client)

if __name__ == "__main__":
    reactor.listenTCP(8080, StarFactory())
    print("Server started. Listening on port 8080...")
    print("Enter client name to register. Enter @ before the starting of a message to send message to another client.")
    reactor.run()
