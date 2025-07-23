from twisted.internet import protocol,reactor

class Echo(protocol.Protocol):
    def connectionMade(self):
        self.msg=input("Enter_msg:")
        self.transport.write(self.msg.encode())

    def dataReceived(self, data):
        print(data.decode())
        self.transport.loseConnection()

class Echofactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()
    
if __name__=="__main__":
    reactor.connectTCP('localhost',8000,Echofactory())
    reactor.run()
