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

def getId(cpf, database = DATABASE):
        ''' function scans database looking for a matching cpf and returns the matched id '''
        data = getDatabase(database)
        for id in data:
                if cpf == data[id][CPF]:
                        return id
        
        return False

def getName(id, database = DATABASE):
        data = getDatabase(database)
        if id in data:
                return data[id][NOME]

def getData(id, database = DATABASE):
        ''' function scans database looking for ID and returns it's table '''
        data = getDatabase(database)
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
        now = str(datetime.now().time())
        time = ''
        for i in range(8):
                time += now[i]
        # Employee register
        data_new = {
                ID: client_id,
                DATA: str(today.strftime("%d/%m/%Y")),
                HORARIO: time,
                QUANTIDADE: quantity,
                PEDIDO: order
        }
        data[employee_id][HISTORICO].append(data_new)
        writeDatabase(data, DATABASE_EMPLOYEES)

        # Client reg
        data_client = getDatabase(DATABASE)
        data_new_client = {
                ID: employee_id,
                DATA: str(today.strftime("%d/%m/%Y")),
                HORARIO: time,
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

def formatCNPJ(cnpj):
        
        cnpj = list(cnpj)
        cnpj.insert(2, '.')
        cnpj.insert(6, '.')
        cnpj.insert(10, '/')
        cnpj.insert(15, '-')

        return ''.join(cnpj)

def formatTelefone(telefone):
        #41 99999-9999
        telefone = list(telefone)
        telefone.insert(2, ' ')
        telefone.insert(8, '-')
        
        return ''.join(telefone)
        
def getHistory(id, database = DATABASE):
        data = getDatabase(database)
        if id in data:
                return data[id][HISTORICO]
                

def getLastHistory(history):
        list = []
        for i in range(len(history)-1, len(history)-4, -1):
                list.append(history[i])
        
        return list

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
