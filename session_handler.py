from datetime import datetime, timedelta
from config import TIMELIMIT


class Connection():
    def __init__(self, ip, id) -> None:
        self.ip = ip
        self.id = id
        self.parceiro = False
        self.cliente = False
        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)


def getConnection(session, ip):
    for connection in session:
        if connection.ip == ip:
            if datetime.now() < connection.expira:
                return connection
            else:
                session.remove(connection)
