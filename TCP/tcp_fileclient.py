from twisted.internet import reactor, protocol

class FileSender(protocol.Protocol):
    def connectionMade(self):
        with open(r"C:\Users\paran\OneDrive\Desktop\paran\TCP\file1.text", "rb") as file:
            for line in file:
                self.transport.write(line.encode())

    def dataReceived(self, data):
        print("Data received:", data.decode())
        # print(len(data.decode()))
        self.transport.loseConnection()

class FileSenderFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return FileSender()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        reactor.stop()

reactor.connectTCP("localhost", 9003, FileSenderFactory())
reactor.run()
