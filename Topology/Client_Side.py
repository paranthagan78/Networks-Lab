from twisted.internet import reactor, protocol
from twisted.internet.defer import DeferredQueue
from twisted.protocols.basic import LineReceiver

class ChatClient(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory
        self.queue = DeferredQueue()

    def connectionMade(self):
        self.factory.client = self
        self.name = input("Enter your name: ")
        self.transport.write(self.name.encode())
        self.queue.get().addCallback(self.send_message)

    def dataReceived(self,data):
        print(data.decode())
        
    def send_message(self, message):
        if message.lower() == 'exit':
            self.transport.loseConnection()
        else:                                  
            self.transport.write(message.encode())
            self.queue.get().addCallback(self.send_message)

class ChatClientFactory(protocol.ClientFactory):
    def __init__(self):
        self.client = None

    def buildProtocol(self, addr):
        return ChatClient(self)
    
    # def startedConnecting(self, connector):
    #     print("Connecting to server...")

    # def clientConnectionLost(self, connector, reason):
    #     print("Connection lost:", reason)

    # def clientConnectionFailed(self, connector, reason):
    #     print("Connection failed:", reason)


def read_input(factory):
    while True:
        if factory.client:
            message = input()
            factory.client.queue.put(message)

if __name__ == "__main__":
    
    factory = ChatClientFactory()
    reactor.connectTCP("localhost", 8080, factory)
    reactor.callInThread(read_input, factory)
    reactor.run()

