from mysql_handler import Mysql
from functions import registerModification
from config import *

print('Bapka Sorvetes - Cupons')
print('Cadastrar um novo parceiro.')

print('Conectando ao banco de dados...\n')
database = Mysql()
database.connect(mysql_bapkasor_cupons)


id = len(database.fetchTable(0, CLIENTES))
loja = input('\nDigite o nome da Loja: ')
cnpj = input('Digite o CNPJ da loja, apenas números: ')
endereco = input('Digite o endereço da loja: ')
telefone = input('Digite o telefone da loja, apenas números: ')
senha = input('Digite a senha de acesso desejada: ')
email = input('Digite um E-mail para vincular: ')

data = (id, loja, cnpj, endereco, telefone, senha, email)
try:
    database.insertParceiro(data, id)
    try:
        database.insertClient(
            (0, 'Placeholder', '12345678901', 0, '41988776655', '123', 'nada@nada.nada'), id)
        for i in range(3):
            registerModification(0, 0, id)
        print('Parceiro cadastrado com sucesso!')

    except:
        print('Houve um erro ao tentar cadastrar o parceiro.')
except:
    print('Houve um erro ao tentar cadastrar o parceiro.')
