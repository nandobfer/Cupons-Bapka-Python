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


def getParceiros():
    ''' function fetch parceiros table and returns a list of dicts with each's name and id '''
    global database
    try:
        data = database.fetchTable(0, 'Parceiros')
        parceiros = []
        for parceiro in data:
            parceiros.append({'id': parceiro[0], 'name': parceiro[1]})
        return parceiros
    except:
        return None


def getName(id, table):
    global database
    try:
        data = database.fetchTable(1, table, 'ID', id)[0]
        name = data[1]
        return name
    except:
        return None


def getData(id, table, parceiro=None):
    ''' function scans database looking for ID and returns it's table '''
    global database
    if parceiro:
        table = f'{parceiro}_{table}'
        print(table)
    try:
        data = database.fetchTable(1, table, 'ID', id)[0]
        if table == CLIENTES:
            formated_data = {
                NOME: data[1],
                CPF: data[2],
                CUPONS: data[3],
                TELEFONE: data[4],
                EMAIL: data[6]
            }
        elif table == PARCEIROS:
            formated_data = {
                NOME: data[1],
                CNPJ: data[2],
                TELEFONE: data[4],
                EMAIL: data[6]
            }

        return formated_data
    except:
        return None


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

    if not database.connection.is_connected():
        database.connect(mysql_bapkasor_cupons)

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
    global database, pedido
    pedido += 1
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
        pedido
    )
    database.insertHistory(data)


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


def getHistory(id, table):
    global database
    column = 'ID_' + table[:-1].upper()
    data = database.fetchTable(0, 'Historicos', column, id)
    return data


def getLastHistory(history, method="", cliente=False):
    count = 1
    incomplete = False
    num_history = len(history)
    lista = []
    id_index = 0
    id_index_name = 1
    table = PARCEIROS
    table_name = CLIENTES
    if cliente:
        id_index = 1
        id_index_name = 0
        table = CLIENTES
        table_name = PARCEIROS

    # for i in range(len(history)-1, len(history)-4, -1):
    for item in history:
        dicionario = {
            ID: item[id_index],
            DATA: item[2],
            HORARIO: item[3],
            QUANTIDADE: item[4],
            PEDIDO: item[5],
            NOME: getName(item[id_index_name], table_name).split()[0]
        }
        lista.append(dicionario)
        count += 1

    # if count > num_history:
    #     incomplete = True
    #     print('incomplete')

    if incomplete or num_history == 0:
        for i in range(4-count):
            dicionario = {
                ID: '',
                DATA: '',
                HORARIO: '',
                QUANTIDADE: 0,
                PEDIDO: '',
                NOME: ''
            }
            lista.append(dicionario)

    # reversing list
    lista = lista[::-1]

    if not method == 'ajax':
        return lista
    else:
        return {"data": lista}


def modifiedCouponHTML(quantity):
    if quantity == 0:
        text = ''
    elif quantity > 0:
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


def signUp(name, telefone, email, cpf, password, parceiro):
    global database
    id = len(database.fetchTable(0, CLIENTES))
    data = (id, name, cpf, 0, telefone, password, email)
    database.insertClient(data, parceiro)


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
pedido = len(database.fetchTable(0, 'Historicos'))
