from twisted.internet import protocol, reactor

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        msg = input("Enter the message to transmit: ")
        self.transport.write(msg.encode())
    
    def dataReceived(self, data):
        print(f"Response from server: {data.decode()}")
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        reactor.stop()

class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()
    
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

# Connect to server
reactor.connectTCP("localhost", 8000, ClientFactory())
reactor.run()
