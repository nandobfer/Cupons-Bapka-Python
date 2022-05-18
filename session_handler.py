

class Connection():
    def __init__(self, ip, id) -> None:
        self.ip = ip
        self.id = id
        self.parceiro = False
        self.cliente = False


def getConnection(session, ip):
    for connection in session:
        if connection.ip == ip:
            return connection
