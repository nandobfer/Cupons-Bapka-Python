from datetime import datetime, timedelta
from config import TIMELIMIT


class Connection():
    def __init__(self, ip, id) -> None:
        self.ip = ip
        self.id = id
        self.parceiro = False
        self.cliente = False
        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True


def getConnection(session, ip):
    for connection in session:
        if connection.ip == ip:
            if not connection.isExpired():
                return connection
            else:
                session.remove(connection)
