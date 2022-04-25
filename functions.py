import json
import re 
from config import *
from datetime import date, datetime

def getDatabase(database = DATABASE):
        with open(database, "r") as read_file:
                data = json.load(read_file)
        return data
    
def writeDatabase(data, database = DATABASE):
    with open(database, "w") as write_file:
            json.dump(data, write_file, indent=4)
    return True

def getId(cpf):
        ''' function scans database looking for a matching cpf and returns the matched id '''
        data = getDatabase()
        for id in data:
                if cpf == data[id][CPF]:
                        return id
        
        return False

def getData(id):
        ''' function scans database looking for ID and returns it's table '''
        data = getDatabase()
        if id in data:
                return data[id]
        
def modifyCoupons(id, quantity: int):
        ''' function adds or removes specified amount of coupons '''
        data = getDatabase()
        data[id][CUPONS] += quantity
        
        # save to database
        writeDatabase(data)
        
def validateId(id):
        if not id:
                return False
        else:
                return True

def clientLogin(telefone, password):
        data = getDatabase()
        for id in data:
                if telefone == data[id][TELEFONE]:
                        if password == data[id][SENHA]:
                                return id
        return False

def employeeLogin(email, password):
        data = getDatabase(DATABASE_EMPLOYEES)
        for id in data:
                if email == data[id][EMAIL]:
                        if password == data[id][SENHA]:
                                return id
        return False

def registerModification(client_id, quantity, employee_id, order):
        data = getDatabase(DATABASE_EMPLOYEES)
        today = date.today()
        now = datetime.now().time()
        # Employee register
        data_new = {
                ID: client_id,
                DATA: str(today.strftime("%d/%m/%Y")),
                HORARIO: str(now),
                QUANTIDADE: quantity,
                PEDIDO: order
        }
        data[employee_id][CUPONS].append(data_new)
        writeDatabase(data, DATABASE_EMPLOYEES)

        # Client reg
        data_client = getDatabase(DATABASE)
        data_new_client = {
                ID: employee_id,
                DATA: str(today.strftime("%d/%m/%Y")),
                HORARIO: str(now),
                QUANTIDADE: quantity,
                PEDIDO: order
        }
        data_client[client_id][HISTORICO].append(data_new_client)
        writeDatabase(data_client, DATABASE)

def formatCPF(cpf):
        cpf = list(cpf)
        cpf.insert(3, '.')
        cpf.insert(7, '.')
        cpf.insert(11, '-')

        return ''.join(cpf)

def formatTelefone(telefone):
        #41 99999-9999
        telefone = list(telefone)
        telefone.insert(2, ' ')
        telefone.insert(8, '-')
        
        return ''.join(telefone)
        

