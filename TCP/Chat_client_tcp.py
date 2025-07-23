from twisted.internet import reactor,protocol
from threading import Thread


receiver=None
class ChatClient(protocol.Protocol):
    def __init__(self):
        global receiver
        receiver=self

    def connectionMade(self):
        print("Client connected successfully")

    def connectionLost(self, reason):
        print("Connection lost due to",reason)

    def dataReceived(self, data):
        print(data.decode())

    def sendMessage(self,msg):
        if self==None:
            print("couldn't speak")
        else:
            self.transport.write(msg.encode())

    def disconnect(self):
        self.transport.loseConnection()

class ChatFactory(protocol.ClientFactory):
    protocol=ChatClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")

    def update(self, data):
        print(data)

class rThread(Thread):
    def __init__(self,host,port):
        Thread.__init__(self)
        self.host=host
        self.port=port
        self.client=ChatClient
        self.factory=ChatFactory()
        self.reactor=reactor

    def run(self):
        self.reactor.connectTCP(self.host,self.port,ChatFactory())
        self.reactor.run(installSignalHandlers=False)

    def stop(self):
        self.reactor.callFromThread(ChatClient.disconnect,receiver)

    def send(self,msg):
        self.reactor.callFromThread(ChatClient.sendMessage,receiver,msg)

    def reconnect(self):
        self.reactor.connectTCP(self.host,self.port,ChatFactory())
        self.reactor.callFromThread(ChatClient.disconnect,receiver)


if __name__=="__main__":
    r=rThread("localhost",8080)
    r.start()

    while True:
        msg=input()
        if msg=="exit":
            r.stop()
        elif msg=="reconnect":
            r.reconnect()
        else:
            r.send(msg)



