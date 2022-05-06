from browser import document, alert, html, bind, ajax
import json

quantity = eval(document["mod-value"].text)

def reset():
        global quantity
        number = document['mod-value']
        sinal = document['sinal']
        
        quantity = 0
        document["mod-value"].text = quantity
        number.style.color = 'white'
        sinal.text =''

@bind(".button-cupons", "click")
def buttonClicked(ev):
    global quantity
    number = document['mod-value']
    sinal = document['sinal']
    
    if not ev.target.id:
        return False
    if ev.target.id == 'buttom-aumentar-shape':
        quantity += 1
        
    elif ev.target.id == 'buttom-diminuir-shape':
        quantity -= 1
        
    if quantity == 0:
        number.style.color = 'white'
        sinal.text =''
    elif quantity > 0:
        number.style.color = 'rgba(32,206,119,1)'
        sinal.style.color = 'rgba(32,206,119,1)'
        sinal.text = '+'
    elif quantity < 0:
        number.style.color = 'rgba(206,32,49,1)'
        sinal.style.color = 'rgba(206,32,49,1)'
        sinal.text = '-'
        
        
    number.text = abs(quantity)
    
def getId():
            id = document.select('.sid')[0].attrs['sid']
            return id
        
def updateHistory(req):
        history = json.loads(req.read())["history"]
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
                                if container.children.index(element) == 0:
                                    for div in element.children:
                                        div_class = div.class_name.split()
                                        if len(div_class) > 1:
                                            if div_class[1] == 'history-data':
                                                    if div_class[0] == 'name_id':
                                                            setIdentification(div, history[index])
                                                    else:
                                                            setHistoryValues(div, history[index], div_class[0])
                                                                        
                                if len(element_class) > 1:
                                        if element_class[1] == 'history-data':
                                                if element_class[0] == 'name_id':
                                                        setIdentification(element, history[index])
                                                else:
                                                        setHistoryValues(element, history[index], element_class[0])
                                                
        setHistory()

def ajaxHistory(id):
        req = ajax.Ajax()
        req.bind('complete', updateHistory)
        req.open('POST', '/history/', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send({"id": id})
    
@bind("#buttom-aplicar", "click")
def modCupom(ev):
    
    global quantity
    
    id = getId()
    employee_id = document["Voltar"].attrs["sid"]
    
    data = {
        "id": id, 
        "quantity": quantity,
        "employee_id": employee_id
    }
    
    def updateData(req):
        new_coupons = json.loads(req.read())
        new_coupons = new_coupons["new_coupons"]
        document["cupons-value"].text = new_coupons
        updateHistory(req)
        
        
    
    def ajaxModCoupons():
        req = ajax.Ajax()
        req.bind('complete', updateData)
        req.open('POST', '/mod_cupons/', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send(data)
            
    if not quantity == 0:
        ajaxModCoupons()
        reset()
    else:
        alert('Valor dos cupons igual a zero.')
        
@bind("#button-limpar", "click")
def resetQuantity(ev):
    reset()
    