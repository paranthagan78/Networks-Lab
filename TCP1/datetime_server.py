from twisted.internet import protocol

class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        print("Data received")
        print(f"Message from client: {data.decode()}")
        
        # Import datetime module
        from datetime import datetime
        
        # Get current date and time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Send current date and time to client
        response = f"Server received '{data.decode()}' at {current_time}"
        self.transport.write(response.encode())

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoServer()

# Run the server
from twisted.internet import reactor

reactor.listenTCP(8000, EchoFactory())
reactor.run()
