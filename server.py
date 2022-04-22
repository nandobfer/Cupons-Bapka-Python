from flask import Flask, escape, request, url_for, redirect, json, render_template
from config import *
from functions import *
import random

app = Flask(__name__)

# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    # redirecting to another endpoint
    return redirect(url_for('home'))

# home page
@app.route('/home/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('employee'):
            return redirect(url_for('loginEmployee'))
        elif request.form.get('client'):
            return redirect(url_for('homeClient'))
    return render_template('index.html')

# client home page
@app.route('/cliente/home/', methods=['GET', 'POST'])
def homeClient():
    if request.method == 'POST':
        telefone = request.form.get('telefone')
        password = request.form.get('password')

        id = clientLogin(telefone, password)
        if not id:
            error = 'E-mail ou senha inválido'
            return render_template('home_client.html', error=error)
        else:
            return redirect(url_for('panelClient', id=id))

    return render_template('home_client.html')

# client panel page
@app.route('/cliente/painel/', methods=['GET', 'POST'])
def panelClient():
    # get id from argument
    try:
        id = request.args.get('id')
    except:
        # error not args
        return redirect(url_for('homeClient'))

    data = getData(id)
    if request.method == 'POST':
        pass

    return render_template('panel_client.html', name=data[NOME], cpf=data[CPF], telefone=data[TELEFONE], cupons=data[CUPONS])

# client history
@app.route('/cliente/historico/', methods=['GET', 'POST'])
def historyClient():
    id = request.args.get('id')
    data = getDatabase()
    data = data[id]

# employee login page
@app.route('/funcionario/login/', methods=['GET', 'POST'])
def loginEmployee():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        id = employeeLogin(email, password)
        if not id:
            error = 'E-mail ou senha inválidos'
            return render_template('login_employee.html', error=error)
        else:
            return redirect(url_for('homeEmployee', employee=id))

    return render_template('login_employee.html')

# home page for employee
@app.route('/funcionario/home/', methods=['GET', 'POST'])
def homeEmployee():
    employee_id = request.args.get('employee')
    if request.method == 'POST':
        cpf = request.form['cpf']
        try:
             id = getId(cpf)

        except:
            # error alert TODO
            return redirect(url_for('homeEmployee'))

        if not id:
            error = 'CPF não encontrado.'
            return render_template('home_employee.html', error=error)
        
        url = url_for('panelEmployee')
        return redirect(f'{url}?id={id}&employee={employee_id}')
    return render_template("home_employee.html")

@app.route('/funcionario/painel/', methods=['GET','POST'])
def panelEmployee():
    # get id's
    id = request.args.get('id')
    employee_id = request.args.get('employee')

    data = getData(id)
    if request.method == 'POST':

        url = url_for('panelEmployee')                         

        try:
            quantity = int(request.form.get('quantity'))
        except:
            # erro alerta insert a quantity number
            return redirect(f'{url}?id={id}&employee={employee_id}') 

        if request.form.get('insert_coupon'):
            modifyCoupons(id, quantity)
            registerModification(id, quantity, employee_id, str(random.randint(0, 1000)))
            return redirect(f'{url}?id={id}&employee={employee_id}')    
        elif request.form.get('remove_coupon'):
            modifyCoupons(id, -quantity)
            registerModification(id, -quantity, employee_id, str(random.randint(0, 1000)))
            return redirect(f'{url}?id={id}&employee={employee_id}')

    if request.form.get('back'):
        url = url_for('homeEmployee')
        print('url', url)
        return redirect(f'{url}?employee={employee_id}')

    ## return render_template("panel_employee.html")
    return render_template("panel_employee.html", name=data[NOME], cpf=data[CPF], telefone=data[TELEFONE], cupons=data[CUPONS], employee_id=employee_id, history=data[HISTORICO])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")

""" flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) """
