from twisted.internet import reactor,protocol

class ChatServer(protocol.Protocol):
    def __init__(self,users):
        self.users=users
        self.name=None
        self.state="GETSTATE"

    def connectionMade(self):
        print("New Client Connected")
        self.transport.write("ENter your name".encode())

    def dataReceived(self, data):
        msg=data.decode()
        if self.state=="GETSTATE":
            self.get_state(msg)       
        elif self.state=="CHAT":
            self.chat(msg)

    def get_state(self,msg):
        self.name=msg
        print("Welcome,",msg)
        self.users[self.name]=self
        self.state="CHAT"

    def chat(self,msg):
        message=f"{self.name}:{msg}".encode()
        for name,client in self.users.items():
            if client!=self:
                client.transport.write(message)
    
class ServerFactory(protocol.Factory):
    def __init__(self):
        self.users={}

    def buildProtocol(self, addr):
        return ChatServer(self.users)
    
if __name__=="__main__":
    reactor.listenTCP(8080,ServerFactory())
    reactor.run()
