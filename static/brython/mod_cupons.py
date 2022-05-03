from browser import document, alert, html, bind

quantity = eval(document["mod-value"].text)

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
    