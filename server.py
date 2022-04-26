import RequirementsHandler
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
        if 'client_panel' in request.form:
            telefone = request.form.get('telefone')
            password = request.form.get('password_client')

            id = clientLogin(telefone, password)
            if not id:
                error = 'Telefone ou senha inválido'
                return render_template('xd_login.html', error=error)
            else:
                return redirect(url_for('panelClient', id=id))
            
        elif 'employee_panel' in request.form:
            email = request.form.get('email')
            password = request.form.get('password_employee')

            id = employeeLogin(email, password)
            if not id:
                error = 'E-mail ou senha inválidos'
                return render_template('xd_login.html', error=error)
            else:
                return redirect(url_for('homeEmployee', employee=id))
        
    return render_template('xd_login.html')

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
    history = getLastHistory(getHistory(id))
    
    # append NOME to history dict
    for i in range(len(history)):
        history[i].update({'Nome': getName(history[i][ID], DATABASE_EMPLOYEES)})
    
    if request.method == 'POST':
        pass

    return render_template('xd_client.html', name=data[NOME], cpf=formatCPF(data[CPF]), telefone=formatTelefone(data[TELEFONE]), cupons=data[CUPONS], id=id,
                           history1_name=history[0][NOME], history1_idp=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]),
                           history2_name=history[1][NOME], history2_idp=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]),
                           history3_name=history[2][NOME], history3_idp=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]))

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
    data = getData(employee_id, DATABASE_EMPLOYEES)
    
    history = getLastHistory(getHistory(id, DATABASE_EMPLOYEES))
    # append NOME to history dict
    for i in range(len(history)):
        history[i].update({'Nome': getName(history[i][ID])})
        
    if request.method == 'POST':
        cpf = request.form['form_cpf']
        try:
             id = getId(cpf)

        except:
            # error alert TODO
            return redirect(url_for('xd_employee'))

        if not id:
            error = 'CPF não encontrado.'
            return render_template('xd_employee.html', error=error)
        
        url = url_for('panelEmployee')
        return redirect(f'{url}?id={id}&employee={employee_id}')
    return render_template("xd_employee.html", name=data[NOME], cpf=formatCPF(data[CPF]), email=data[EMAIL], employee_id=employee_id)

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

        if 'insert_coupon' in request.form:
            modifyCoupons(id, quantity)
            registerModification(id, quantity, employee_id, str(random.randint(0, 1000)))
            return redirect(f'{url}?id={id}&employee={employee_id}')    
        elif 'remove_coupon' in request.form:
            modifyCoupons(id, -quantity)
            registerModification(id, -quantity, employee_id, str(random.randint(0, 1000)))
            return redirect(f'{url}?id={id}&employee={employee_id}')

    if request.form.get('back'):
        url = url_for('homeEmployee')
        print('url', url)
        return redirect(f'{url}?employee={employee_id}')

    ## return render_template("panel_employee.html")
    return render_template("xd_employee_client.html", name=data[NOME], cpf=formatCPF(data[CPF]), telefone=formatTelefone(data[TELEFONE]), cupons=data[CUPONS], employee_id=employee_id, history=data[HISTORICO])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")

""" flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) """
