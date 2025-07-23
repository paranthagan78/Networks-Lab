import subprocess
from twisted.internet import reactor, defer

class Traceroute:
    def __init__(self):
        self.deferred = defer.Deferred()

    def traceroute(self, host):
        process = subprocess.Popen(['traceroute', '-m', '10', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            self.deferred.errback(error)
        else:
            self.deferred.callback(output)

def print_result(result):
    print(result.decode())

def print_error(failure):
    print(failure)

protocol = Traceroute()
protocol.traceroute('google.com')
protocol.deferred.addCallbacks(print_result, print_error)
reactor.run()
