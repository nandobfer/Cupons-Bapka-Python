from browser import document, ajax, html, bind, window


class Parceiro():
    def __init__(self, data) -> None:
        self.id = data[0]
        self.name = data[1]


def appendStore(parceiro):
    container = document['lojas']
    element = html.BUTTON(f'{parceiro.name}',
                          Id=f'button-{parceiro.id}', Class='button')
    # element.classList.add("button")

    container <= element

    @bind(f"#button-{parceiro.id}", "click")
    def chooseStore(ev):
        print(parceiro.name)

        data = {
            'loja': parceiro.id
        }

        ajaxChooseStore(data)


def getParceiros(req):
    parceiros = eval(req.text)
    print(parceiros)
    print(type(parceiros))

    for item in parceiros:
        parceiro = Parceiro(item)
        appendStore(parceiro)


def hideButtons():
    buttons = document.select(".button")
    for element in buttons:
        element.style.display = 'none'
        element.style.visibility = 'hidden'

    element = html.P(f'Carregando')
    element.style.color = 'white'
    element.style.fontSize = "32px"
    # element.classList.add("button")

    document['lojas'] <= element


def redirect(req):
    response = eval(req.text)
    if response:
        hideButtons()
        # document["result"].html = req.text  # Commented out example code.
        window.location.href = "/cliente/painel/"
    else:
        window.location.href = "/home/?error=1"


def ajaxChooseStore(data):
    req = ajax.Ajax()
    req.bind('complete', redirect)
    req.open('POST', '/cliente/loja/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send(data)


def ajaxPopulateButtons():
    req = ajax.Ajax()
    req.bind('complete', getParceiros)
    req.open('POST', '/parceiros/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send('test')


ajaxPopulateButtons()
