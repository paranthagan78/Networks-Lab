from twisted.internet import reactor, protocol


class StopServer(protocol.Protocol):
    def send_ack(self):
        self.transport.write(input("Enter ack(ack/ACK): ").encode())

    def dataReceived(self, data):
        print("Message from client:", data.decode())
        ack = f'{"Server recieved - " + data.decode()}'
        self.send_ack()

    def connectionLost(self, reason):
        print("Client disconnected:")


class StopAndWaitServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return StopServer()


reactor.listenTCP(8000, StopAndWaitServerFactory())
reactor.run()
