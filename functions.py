import json
from config import *
from datetime import date, datetime
from mysql_handler import Mysql


def getDatabase(database=DATABASE):
    with open(database, "r") as read_file:
        data = json.load(read_file)
    return data


def getTable(table):
    database = Mysql()
    database.connect(mysql_bapkasor_cupons)
    data = database.fetchTable(0, table)
    return data


def writeDatabase(data, database=DATABASE):
    with open(database, "w") as write_file:
        json.dump(data, write_file, indent=4)
    return True


def getId(cpf, table):
    ''' function scans database looking for a matching cpf and returns the matched id '''
    global database
    try:
        data = database.fetchTable(1, table, "CPF", cpf)[0]
        id = data[0]
        return str(id)
    except:
        return None


def getName(id, database=DATABASE):
    data = getDatabase(database)
    if id in data:
        return data[id][NOME]


def getData(id, table):
    ''' function scans database looking for ID and returns it's table '''
    global database
    data = database.fetchTable(1, table, 'ID', id)[0]
    print(data)
    if table == CLIENTES:
        formated_data = {
            NOME: data[1],
            CPF: data[2],
            CUPONS: data[3],
            TELEFONE: data[4]
        }
    elif table == PARCEIROS:
        formated_data = {
            NOME: data[1],
            CNPJ: data[2],
            TELEFONE: data[4],
            EMAIL: data[6]
        }

    return formated_data


def modifyCoupons(id, quantity: int):
    ''' function adds or removes specified amount of coupons '''
    global database
    data = database.fetchTable(1, CLIENTES, 'ID', id)[0]
    cupons = data[3] + quantity

    # save to database
    database.updateTable(CLIENTES, id, 'CUPONS', cupons, 'ID')
    return cupons


def validateId(id):
    if not id:
        return False
    else:
        return True


def userLogin(user, try_password, table):
    global database
    data = False
    try:
        if table == CLIENTES:
            data = database.fetchTable(1, table, 'TELEFONE', user)[0]
        elif table == PARCEIROS:
            data = database.fetchTable(1, table, 'EMAIL', user)[0]
        if data:
            password = data[5]
    except Exception as error:
        print(error)
        return None
    if try_password == password:
        id = data[0]
        return str(id)


def employeeLogin(email, password):
    data = getDatabase(DATABASE_EMPLOYEES)
    for id in data:
        if email == data[id][EMAIL]:
            if password == data[id][SENHA]:
                return id
    return False


def registerModification(client_id, quantity, employee_id, order):
    global database
    today = date.today()
    formated_today = str(today.strftime("%d/%m/%Y"))
    now = str(datetime.now().time())
    time = ''
    for i in range(8):
        time += now[i]
    data = (
        employee_id,
        client_id,
        formated_today,
        time,
        quantity,
        order
    )
    database.insertHistory(data)
    # data = getDatabase(DATABASE_EMPLOYEES)
    # today = date.today()
    # now = str(datetime.now().time())
    # time = ''
    # for i in range(8):
    #     time += now[i]
    # # Employee register
    # data_new = {
    #     ID: client_id,
    #     DATA: str(today.strftime("%d/%m/%Y")),
    #     HORARIO: time,
    #     QUANTIDADE: quantity,
    #     PEDIDO: order
    # }
    # data[employee_id][HISTORICO].append(data_new)
    # writeDatabase(data, DATABASE_EMPLOYEES)

    # # Client reg
    # data_client = getDatabase(DATABASE)
    # data_new_client = {
    #     ID: employee_id,
    #     DATA: str(today.strftime("%d/%m/%Y")),
    #     HORARIO: time,
    #     QUANTIDADE: quantity,
    #     PEDIDO: order
    # }
    # data_client[client_id][HISTORICO].append(data_new_client)
    # writeDatabase(data_client, DATABASE)


def formatCPF(cpf):
    cpf = list(cpf)
    cpf.insert(3, '.')
    cpf.insert(7, '.')
    cpf.insert(11, '-')

    return ''.join(cpf)


def formatCNPJ(cnpj):

    cnpj = list(cnpj)
    cnpj.insert(2, '.')
    cnpj.insert(6, '.')
    cnpj.insert(10, '/')
    cnpj.insert(15, '-')

    return ''.join(cnpj)


def formatTelefone(telefone):
    # 41 99999-9999
    telefone = list(telefone)
    telefone.insert(2, ' ')
    telefone.insert(8, '-')

    return ''.join(telefone)


def getHistory(id, database=DATABASE):
    data = getDatabase(database)
    print(id)
    if id in data:
        return data[id][HISTORICO]


def getLastHistory(history, method=""):
    list = []
    for i in range(len(history)-1, len(history)-4, -1):
        list.append(history[i])

    if not method == 'ajax':
        return list
    else:
        return {"data": list}


def modifiedCouponHTML(quantity):
    if quantity > 0:
        if quantity == 1:
            text = 'Adicionado'
        else:
            text = 'Adicionados'
    else:
        if quantity == -1:
            text = 'Removido'
        else:
            text = 'Removidos'
    return text


def signUp(name, telefone, email, cpf, password):
    global database
    id = len(database.fetchTable(0, CLIENTES))
    data = (id, name, cpf, 0, telefone, password, email)
    database.insertClient(data)


def isCliente(session, id, ip):
    connection = {
        str(ip): (id, 'cliente')
    }
    if connection in session:
        print(connection)
        print(session)
        return True


def getSession(session, ip):
    ip = str(ip)
    for connection in session:
        if ip in connection:
            return connection[ip][0]


database = Mysql()
database.connect(mysql_bapkasor_cupons)
