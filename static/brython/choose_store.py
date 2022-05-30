from browser import document, ajax, html
import json


def appendStore(parceiro):
    global n
    container = document['lojas']
    element = html.BUTTON(f'{parceiro["name"]}')
    element.classList.add("button")

    container <= element


def getParceiros(req):
    parceiros = eval(req.text)
    print(parceiros)
    print(type(parceiros))

    for parceiro in parceiros:
        appendStore(parceiro)


def ajaxParceiros():
    req = ajax.Ajax()
    req.bind('complete', getParceiros)
    req.open('POST', '/parceiros/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send('test')


ajaxParceiros()
