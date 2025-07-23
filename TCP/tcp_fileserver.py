from twisted.internet import reactor, protocol

class FileReceiver(protocol.Protocol):
    def dataReceived(self, data):
        print("Data received:", data.decode())
        
        with open("file2.txt", "ab") as file:
            file.write(data)
        self.transport.write(data)

class FileReceiverFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return FileReceiver()

reactor.listenTCP(9003, FileReceiverFactory())
reactor.run()
