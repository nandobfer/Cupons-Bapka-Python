import RequirementsHandler
from flask import Flask, request, url_for, redirect, render_template, request
from config import *
from functions import *
import random

session = []

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
        global session
        if 'client_panel' in request.form:
            telefone = request.form.get('telefone')
            password = request.form.get('password_client')

            id = userLogin(telefone, password, CLIENTES)
            if not id:
                error = 'Não foi possível encontrar uma conta com esse número de telefone.'
                return render_template('login_desktop.html', error_client=error)
            else:
                login = {
                    str(request.remote_addr): id
                }
                session.append(login)
                return redirect(url_for('panelClient'))

        elif 'employee_panel' in request.form:
            email = request.form.get('email')
            password = request.form.get('password_employee')

            id = userLogin(email, password, PARCEIROS)
            print(id)
            if not id:
                error = 'Não foi possível encontrar uma conta com esse email. Por favor, entre em contato com o administrador para recuperar o acesso.'
                return render_template('login_desktop.html', error_partner=error)
            else:
                login = {
                    str(request.remote_addr): id
                }
                session.append(login)
                return redirect(url_for('homeEmployee', employee=id))

    elif request.method == 'GET':
        session.pop(str(request.remote_addr))

    return render_template('login_desktop.html')

# client panel page


@app.route('/cliente/painel/', methods=['GET', 'POST'])
def panelClient():
    global session
    try:
        id = getSession(session, request.remote_addr)
    except:
        return redirect(url_for('home'))

    print(session, id, request.remote_addr)
    if not isLoggedIn(session, id, request.remote_addr):
        return redirect(url_for('home'))

    data = getData(id)
    history = getLastHistory(getHistory(id))

    # append NOME to history dict
    for i in range(len(history)):
        history[i].update(
            {'Nome': getName(history[i][ID], DATABASE_EMPLOYEES)})

    if request.method == 'POST':
        pass

    return render_template('cliente_desktop.html', history=history, name=data[NOME], cpf=formatCPF(data[CPF]), telefone=formatTelefone(data[TELEFONE]), cupons=data[CUPONS], id=id,
                           history1_name=history[0][NOME], history1_idp=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                           history2_name=history[1][NOME], history2_idp=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                           history3_name=history[2][NOME], history3_idp=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))

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

    history = getLastHistory(getHistory(employee_id, DATABASE_EMPLOYEES))
    # append NOME to history dict
    for i in range(len(history)):
        history[i].update({'Nome': getName(history[i][ID])})

    if request.method == 'POST':
        cpf = request.form['form_cpf']
        try:
            id = getId(cpf)

        except:
            # error alert TODO
            return redirect(url_for('home'))

        if not id:
            error = 'Não foi possível encontrar uma conta com esse nome de usuário.'
            return render_template('parceiro_desktop.html', name=data[NOME], cnpj=formatCNPJ(data[CNPJ]), email=data[EMAIL], employee_id=employee_id, telefone=formatTelefone(data[TELEFONE]), error=error,
                                   history1_name=history[0][NOME], history1_idc=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                                   history2_name=history[1][NOME], history2_idc=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                                   history3_name=history[2][NOME], history3_idc=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))

        url = url_for('panelEmployee')
        return redirect(f'{url}?id={id}&employee={employee_id}')
    return render_template("parceiro_desktop.html", name=data[NOME], cnpj=formatCNPJ(data[CNPJ]), email=data[EMAIL], employee_id=employee_id, telefone=formatTelefone(data[TELEFONE]),
                           history1_name=history[0][NOME], history1_idc=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                           history2_name=history[1][NOME], history2_idc=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                           history3_name=history[2][NOME], history3_idc=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))


@app.route('/funcionario/painel/', methods=['GET', 'POST'])
def panelEmployee():
    # get id's
    id = request.args.get('id')
    employee_id = request.args.get('employee')

    data = getData(id)

    history = getLastHistory(getHistory(id))
    # append NOME to history dict
    for i in range(len(history)):
        history[i].update(
            {'Nome': getName(history[i][ID], DATABASE_EMPLOYEES)})

    if request.method == 'POST':

        url = url_for('panelEmployee')

        try:
            quantity = int(request.form.get('quantity'))
        except:
            # erro alerta insert a quantity number
            return redirect(f'{url}?id={id}&employee={employee_id}')

        if 'insert_coupon' in request.form:
            modifyCoupons(id, quantity)
            registerModification(id, quantity, employee_id,
                                 str(random.randint(0, 1000)))
            return redirect(f'{url}?id={id}&employee={employee_id}')
        elif 'remove_coupon' in request.form:
            modifyCoupons(id, -quantity)
            registerModification(id, -quantity, employee_id,
                                 str(random.randint(0, 1000)))
            return redirect(f'{url}?id={id}&employee={employee_id}')

    if request.form.get('back'):
        url = url_for('homeEmployee')
        return redirect(f'{url}?employee={employee_id}')

    # return render_template("panel_employee.html")
    return render_template("parceiro_cliente_desktop.html", name=data[NOME], client_id=id, cpf=formatCPF(data[CPF]), telefone=formatTelefone(data[TELEFONE]), cupons=data[CUPONS], employee_id=employee_id,
                           history1_name=history[0][NOME], history1_idp=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                           history2_name=history[1][NOME], history2_idp=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                           history3_name=history[2][NOME], history3_idp=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))


@app.route('/funcionario/cadastro/', methods=['GET', 'POST'])
def signUpPage():
    if request.method == 'POST':
        if 'signup' in request.form:
            try:
                name = request.form.get('name')
                telefone = request.form.get('telefone')
                email = request.form.get('email')
                cpf = request.form.get('cpf')
                password = request.form.get('password')
                password_confirmation = request.form.get(
                    'password-confirmation')
                if not password == password_confirmation:
                    error = 'Não foi possível encontrar uma conta com esse nome de usuário. Podemos ajudá-lo a recuperar seu nome de usuário?'
                    return render_template('cadastro_desktop.html', error=error)

                signUp(name, telefone, email, cpf, password)
                error = 'Usuário cadastrado com sucesso!'
                return render_template('cadastro_desktop.html', error=error)
            except Exception as e:
                # erro alerta insert a quantity number
                error = 'Não foi possível encontrar uma conta com esse nome de usuário. Podemos ajudá-lo a recuperar seu nome de usuário?'
                return render_template('cadastro_desktop.html', error=error)

        elif 'voltar' in request.form:
            print('oi', request.remote_addr)

    return render_template("cadastro_desktop.html")


@app.route('/cliente/recuperar_senha/', methods=['GET', 'POST'])
def recoverPass():

    return render_template("recover.html")


@app.route('/cliente/alterar_telefone/', methods=['GET', 'POST'])
def changePhone():
    data = getData("00")

    return render_template("alterar.html", data=data)


@app.route('/history/', methods=['POST'])
def history():
    if request.method == 'POST':
        if 'id' in request.form:
            id = request.form["id"]
            # id = data["id"]
            history = getLastHistory(getHistory(id), 'ajax')
            # append NOME to history dict
            for i in range(len(history["data"])):
                history["data"][i].update(
                    {'Nome': getName(history["data"][i][ID])})
            return history


@app.route('/mod_cupons/', methods=(['POST']))
def modCupons():

    if request.method == 'POST':
        if 'id' in request.form:
            id = request.form["id"]
            quantity = int(request.form["quantity"])
            employee_id = request.form["employee_id"]

            new_coupons = modifyCoupons(id, quantity)
            registerModification(id, quantity, employee_id, 0)

            history = getLastHistory(getHistory(id))
            # append NOME to history dict
            for i in range(len(history)):
                history[i].update({'Nome': getName(history[i][ID])})

            result = {
                "history": history,
                "new_coupons": new_coupons
            }
            return result


@app.route('/database.json', methods=['GET'])
def database():
    return getDatabase()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")

""" flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) """
