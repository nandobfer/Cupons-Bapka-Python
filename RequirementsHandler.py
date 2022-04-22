import os, importlib

def readRequirements():
    with open("requirements.txt", "r") as file:
            file = file.read()
            requirements = file.split('\n')
    return requirements

def getRequirements():
    requirements = readRequirements()
    for requirement in requirements:
        try:
            installModule(requirement)
        except:
            print(f'Não foi possivel baixar o modulo: {requirement}')

def installModule(requirement):
    # MODULO PyPDF2
    try:
        module = importlib.import_module(requirement)
        print(f'Modulo {requirement} ja instalado')
        return True
    except:
        print(f'Modulo nao encontrado: {requirement}')
        print(f'Tentando instalar automaticamente')
        try:
            os.system(f'pip install {requirement}')
            print(f'Modulo instalado: {requirement}')
            return True
        except:
            return False
