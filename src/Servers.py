class Server:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        
    def save(self):
        return {'name':self.name, 'ip':self.ip, 'port':self.port}