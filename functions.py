import json 
from config import *

def getDatabase():
        with open(DATABASE, "r") as read_file:
                data = json.load(read_file)
        return data
    
def writeDatabase(data):
    with open(DATABASE, "w") as write_file:
            json.dump(data, write_file, indent=4)
    return True

def getId(cpf):
        ''' function scans database looking for a matching cpf and returns the matched id '''
        data = getDatabase()
        for id in data:
                if cpf in data[id]:
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
        