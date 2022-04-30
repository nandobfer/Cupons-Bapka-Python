from browser import document, alert

def test(num):
    return num+1

def hello(ev):
    element = document["py"]
    num = element.attrs["num"]
    ada = test(int(num))
    alert(ada)

document["button_alert"].bind("click", hello)