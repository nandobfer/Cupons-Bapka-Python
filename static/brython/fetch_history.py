from browser import document, ajax
import json


def on_complete(req):
    history = json.loads(req.text)["data"]
    config = {
        'date': 'Data',
        'time': "Hor\u00e1rio",
        'quantidades': "Quantidade"
    }

    def setIdentification(element, data):
        name = data['Nome']
        id = data['Id']
        element.textContent = f'{name} - IDP: {id}'

    def setHistoryValues(element, data, key):
        if key == 'mod-cupons':
            if data['Quantidade'] > 0:
                if data['Quantidade'] == 1:
                    text = 'Adicionado'
                else:
                    text = 'Adicionados'
                element.style.color = "rgba(32,206,119,1)"
            elif data['Quantidade'] < 0:
                if data['Quantidade'] == -1:
                    text = 'Removido'
                else:
                    text = 'Removidos'
                element.style.color = "rgba(206,32, 49,1)"
            elif data['Quantidade'] == 0:
                text = ''
            element.textContent = text

        elif key == 'quantidades':
            element.textContent = abs(data[config[key]])
        else:
            element.textContent = data[config[key]]

        def setHistory():
            for container in document.select('.history'):
                index = document.select('.history').index(container)

                for element in container.children:
                    element_class = element.class_name.split()
                    if len(element_class) > 1:
                        if element_class[1] == 'history-data':
                            if element_class[0] == 'name_id':
                                setIdentification(element, history[index])
                            else:
                                setHistoryValues(
                                    element, history[index], element_class[0])

        setHistory()


def ajaxHistory(id):
    req = ajax.Ajax()
    req.bind('complete', on_complete)
    req.open('POST', '/history/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({"id": id})


def getId():
    id = document.select('.sid')[0].attrs['sid']
    return id


ajaxHistory(getId())
