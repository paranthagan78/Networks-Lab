from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        print("Received data:",data)
        self.transport.write(data)

class EchoFatory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

if __name__=="__main__":
    reactor.listenTCP(8000,EchoFatory())
    print("Server started to listen")
    reactor.run()
