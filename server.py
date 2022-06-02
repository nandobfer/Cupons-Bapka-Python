import reqcheq
from flask import Flask, request, url_for, redirect, render_template, request
from config import *
from functions import *
import random
from session_handler import *

clientes = []
session = []
parceiros = getParceiros()

app = Flask(__name__)

# index page


@app.route('/', methods=['GET', 'POST'])
def index():
    # redirecting to another endpoint
    return redirect(url_for('home'))

# home page


@app.route('/home/', methods=['GET', 'POST'])
def home():
    ip = str(request.remote_addr)
    if request.method == 'POST':
        global session, clientes
        if 'client_panel' in request.form:
            telefone = request.form.get('telefone')
            password = request.form.get('password_client')

            clientes.append({ip: (telefone, password)})

            return redirect(url_for('chooseStore'))

        elif 'employee_panel' in request.form:
            email = request.form.get('email')
            password = request.form.get('password_employee')

            id = userLogin(email, password, PARCEIROS)
            print(id)
            if not id:
                error = 'Não foi possível encontrar uma conta com esse email. Por favor, entre em contato com o administrador para recuperar o acesso.'
                return render_template('login_desktop.html', error_partner=error)
            else:
                login = Connection(ip, id)
                login.parceiro = True
                session.append(login)
                return redirect(url_for('homeEmployee'))

    elif request.method == 'GET':

        error = request.args.get('error')
        if error:
            error = 'Não foi possível encontrar uma conta com esse número de telefone.'
        else:
            error = ''

        for connection in session:
            if connection.ip == ip:
                session.remove(connection)

    return render_template('login_desktop.html', error_client=error)


@app.route('/cliente/loja/', methods=['GET', 'POST'])
def chooseStore():
    global session, clientes
    ip = str(request.remote_addr)

    if request.method == 'POST':
        for item in clientes:
            if ip in item:
                telefone = item[ip][0]
                senha = item[ip][1]
                clientes.remove(item)

        loja = request.form['loja']

        id = userLogin(telefone, senha, CLIENTES, loja)
        if not id:
            error = 'Não foi possível encontrar uma conta com esse número de telefone.'
            return 'False'
        else:
            login = Connection(ip, id, loja)
            login.cliente = True
            # login = {
            #     str(request.remote_addr): (id, 'cliente')
            # }
            session.append(login)
            return 'True'

    return render_template('choose_store_desktop.html')


# client panel page


@app.route('/cliente/painel/', methods=['GET', 'POST'])
def panelClient():
    global session
    ip = str(request.remote_addr)
    try:
        connection = getConnection(session, ip)
        id = connection.id
        loja = connection.loja
    except:
        return redirect(url_for('home'))

    if not connection.cliente:
        return redirect(url_for('home'))

    data = getData(id, CLIENTES, loja)
    history = getLastHistory(id, CLIENTES, cliente=True)

    if request.method == 'POST':
        pass

    if history:
        return render_template('cliente_desktop.html', history=history, name=data[NOME].split()[0], cpf=formatCPF(data[CPF]), telefone=formatTelefone(data[TELEFONE]), cupons=data[CUPONS], email=data[EMAIL], id=id,
                               history1_name=history[0][NOME], history1_idp=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                               history2_name=history[1][NOME], history2_idp=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                               history3_name=history[2][NOME], history3_idp=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))
    else:
        return render_template('cliente_desktop.html', history=history, name=data[NOME].split()[0], cpf=formatCPF(data[CPF]), telefone=formatTelefone(data[TELEFONE]), cupons=data[CUPONS], id=id)

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
    global session
    ip = str(request.remote_addr)
    try:
        # id = getSession(session, request.remote_addr)
        connection = getConnection(session, ip)
        employee_id = connection.id
    except:
        return redirect(url_for('home'))

    if not connection.parceiro:
        return redirect(url_for('home'))

    data = getData(employee_id, PARCEIROS)

    history = getLastHistory(employee_id, PARCEIROS)

    if request.method == 'POST':
        cpf = request.form['form_cpf']
        try:
            id = getId(cpf, CLIENTES, parceiro=employee_id)
            print(id)

        except:
            pass

        if not id:
            error = 'Não foi possível encontrar um cliente com esse CPF nesta loja.'
            return render_template('parceiro_desktop.html', name=data[NOME], cnpj=formatCNPJ(data[CNPJ]), email=data[EMAIL], employee_id=employee_id, telefone=formatTelefone(data[TELEFONE]), error=error,
                                   history1_name=history[0][NOME], history1_idc=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                                   history2_name=history[1][NOME], history2_idc=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                                   history3_name=history[2][NOME], history3_idc=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))
        else:
            url = url_for('panelEmployee')
            return redirect(f'{url}?id={id}')
    return render_template("parceiro_desktop.html", name=data[NOME].split()[0], cnpj=formatCNPJ(data[CNPJ]), email=data[EMAIL], employee_id=employee_id, telefone=formatTelefone(data[TELEFONE]),
                           history1_name=history[0][NOME], history1_idc=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                           history2_name=history[1][NOME], history2_idc=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                           history3_name=history[2][NOME], history3_idc=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))


@app.route('/funcionario/painel/', methods=['GET', 'POST'])
def panelEmployee():
    # get id's
    global session
    id = request.args.get('id')
    ip = str(request.remote_addr)
    try:
        connection = getConnection(session, ip)
        employee_id = connection.id
    except:
        return redirect(url_for('home'))

    if not connection.parceiro:
        return redirect(url_for('home'))

    data = getData(id, CLIENTES, employee_id)

    history = getLastHistory(id, CLIENTES, cliente=True)

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
        return redirect(f'{url}')

    # return render_template("panel_employee.html")
    return render_template("parceiro_cliente_desktop.html", name=data[NOME].split()[0], client_id=id, cpf=formatCPF(data[CPF]), telefone=formatTelefone(data[TELEFONE]), cupons=data[CUPONS], employee_id=employee_id,
                           history1_name=history[0][NOME], history1_idp=history[0][ID], history1_data=history[0][DATA], history1_time=history[0][HORARIO], history1_quantity=history[0][QUANTIDADE], history1_modified=modifiedCouponHTML(history[0][QUANTIDADE]), history1_quantity_abs=abs(history[0][QUANTIDADE]),
                           history2_name=history[1][NOME], history2_idp=history[1][ID], history2_data=history[1][DATA], history2_time=history[1][HORARIO], history2_quantity=history[1][QUANTIDADE], history2_modified=modifiedCouponHTML(history[1][QUANTIDADE]), history2_quantity_abs=abs(history[1][QUANTIDADE]),
                           history3_name=history[2][NOME], history3_idp=history[2][ID], history3_data=history[2][DATA], history3_time=history[2][HORARIO], history3_quantity=history[2][QUANTIDADE], history3_modified=modifiedCouponHTML(history[2][QUANTIDADE]), history3_quantity_abs=abs(history[2][QUANTIDADE]))


@app.route('/funcionario/cadastro/', methods=['GET', 'POST'])
def signUpPage():
    global session
    ip = str(request.remote_addr)
    try:
        connection = getConnection(session, ip)
        id = connection.id
    except:
        return redirect(url_for('home'))

    if not connection.parceiro:
        return redirect(url_for('home'))

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

                signUp(name, telefone, email, cpf, password, id)
                error = 'Usuário cadastrado com sucesso!'
                return render_template('cadastro_desktop.html', error=error)
            except Exception as e:
                # erro alerta insert a quantity number
                error = 'Não foi possível encontrar uma conta com esse nome de usuário. Podemos ajudá-lo a recuperar seu nome de usuário?'
                return render_template('cadastro_desktop.html', error=e)

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
            history = getLastHistory(id, CLIENTES, 'ajax', True)
            return history


@app.route('/mod_cupons/', methods=(['POST']))
def modCupons():

    if request.method == 'POST':
        if 'id' in request.form:
            id = request.form["id"]
            quantity = int(request.form["quantity"])
            employee_id = request.form["employee_id"]

            new_coupons = modifyCoupons(id, employee_id, quantity)
            registerModification(id, quantity, employee_id,
                                 random.random()*1000)

            history = getLastHistory(id, CLIENTES, cliente=True)

            result = {
                "history": history,
                "new_coupons": new_coupons
            }
            return result


@app.route('/database.json', methods=['GET'])
def database():
    return getDatabase()


@app.route('/parceiros/', methods=['POST'])
def parceiros_route():
    global parceiros
    return str(parceiros)


@app.route('/flushparceiros/', methods=['POST'])
def flush_parceiros_route():
    global parceiros
    try:
        parceiros = getParceiros()
        return 'parceiros flushed'
    except Exception as error:
        return str(error)


@app.route('/session/', methods=['GET', 'POST'])
def sessionurl():
    global session
    formated_session = []
    for connection in session:
        formated_session.append(
            (connection.ip, connection.id, connection.loja))
    return str(formated_session)


@app.route('/clientes/', methods=['GET', 'POST'])
def clientesurl():
    global clientes
    return str(clientes)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")

""" flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) """
