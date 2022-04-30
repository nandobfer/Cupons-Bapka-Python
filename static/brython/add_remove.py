from browser import document, alert
from ast import literal_eval

history = literal_eval(document['add_remove'].attrs['history'])
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
                else:
                        if data['Quantidade'] == -1:
                                text = 'Removido'
                        else:
                                text = 'Removidos'
                        element.style.color = "rgba(206,32, 49,1)"
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
                                                setHistoryValues(element, history[index], element_class[0])
                                        
setHistory()