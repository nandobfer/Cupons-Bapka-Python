import os, json
from functions import *
from config import *

class Client():
    def __init__(self, id) -> None:
        self.id = id
        

    def login(self):
        try:
            self.json = getDatabase()
            self.data = self.json[str(self.id)]
            return True
        except:
            return False

    def printDados(self):
        os.system('cls')
        print("Dados do cliente:")
        for key in self.data:
            print(f'{key}: {self.data[key]}')


    def addCupom(self, quantity):
        self.data[CUPONS] += quantity
        print(f'Adicionando {quantity} cupom(s) para {self.data[NOME]}')
        print(f'Cupons: {self.data[CUPONS]}')

        self.json[str(id)] = self.data
        with open(DATABASE, "w") as write_file:
            json.dump(self.json, write_file, indent=4)

    def removerCupom(self, quantity):
        self.data[CUPONS] -= quantity
        if self.data[CUPONS] < 0:
            self.data[CUPONS] = 0
        print(f'Removendo {quantity} cupom(s) de {self.data[NOME]}')
        print(f'Cupons: {self.data[CUPONS]}')

        self.json[str(id)] = self.data
        with open(DATABASE, "w") as write_file:
            json.dump(self.json, write_file, indent=4)

    def cadastrar(self):
        nome = input('Digite seu nome: ')
        cpf = input('Digite seu CPF: ')
        email = input('Digite seu e-mail: ')
        cupons = 0
        self.json[str(self.id)] = {
            NOME: nome,
            CPF: cpf,
            EMAIL: email,
            CUPONS: cupons
        }
        with open(DATABASE, "w") as write_file:
            json.dump(self.json, write_file, indent=4)
