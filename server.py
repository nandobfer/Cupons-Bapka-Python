from flask import Flask, escape, request, url_for, redirect, json, render_template
from config import *
from functions import *

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
            return redirect(url_for('homeEmployee'))
        elif request.form.get('client'):
            return redirect(url_for('homeClient'))
    return render_template('index.html')

# client home page
@app.route('/cliente/home/', methods=['GET', 'POST'])
def homeClient():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        id = clientLogin(email, password)
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

    return render_template('panel_client.html', name=data[NOME], cpf=data[CPF], email=data[EMAIL], cupons=data[CUPONS])

# home page for employee
@app.route('/funcionario/home/', methods=['GET', 'POST'])
def homeEmployee():
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
        
        return redirect(url_for('panelEmployee', id=id))
    return render_template("home_employee.html")

@app.route('/funcionario/painel/', methods=['GET','POST'])
def panelEmployee():
    try:
        id = request.args.get('id')
    except:
        return redirect(url_for('homeEmployee'))
    
    data = getData(id)
    if request.method == 'POST':

        try:
            quantity = int(request.form.get('quantity'))
        except:
            # erro alerta insert a quantity number
            return redirect(url_for('panelEmployee', id=id))
                                  
        if request.form.get('insert_coupon'):
            modifyCoupons(id, quantity) 
            return redirect(url_for('panelEmployee', id=id))    
        elif request.form.get('remove_coupon'):
            modifyCoupons(id, -quantity) 
            print('menos')
            return redirect(url_for('panelEmployee', id=id))    
        elif request.form.get('redirect_home'):
            print('deu')
            return redirect(url_for('index'))

    # return render_template("panel_employee.html")
    return render_template("panel_employee.html", name=data[NOME], cpf=data[CPF], email=data[EMAIL], cupons=data[CUPONS])

# @app.route('/homeuser/', methods=['GET', 'POST'])
# def homeuser():
#     # checar se foi passado um id ou não
#     id = request.args.get('id')
#     if not id:
#         return redirect(url_for('home'))

#     if request.method == 'POST':
#         if request.form.get('action1') == 'Ver dados':
#             return redirect(url_for('userPage', id=id))
#         elif request.form.get('action2') == 'Sair':
#             return redirect(url_for('home'))
#         else:
#             pass # unknown
#     elif request.method == 'GET':
#         return render_template('home_user.html', user = id)
#     return render_template("home_user.html", user=id)

# url/argument=name
# @app.route('/<name>/')
# def hello(name):
#     # print on page "Hello, argument passed on URL!"
#     return f'<h1>Hello, {escape(name)}!</h1>'

# console printing
# with app.test_request_context():
#     print(url_for('home'))
#     # url_for('functionName', functionArgs = 'args')
#     print(url_for('hello', name='Fernando'))
    
# write at database
# @app.route('/save/', methods=['GET', 'POST'])
# def saveUser():
#     # id = request.args.get('id')
#     new_data = json.loads(request.args.get('data'))
#     data = readJSON(DATABASE)
#     data[new_data['Usuário']] = new_data
#     writeJSON(data, DATABASE)
#     return '<h1>Success</h1>'

# # user page
# @app.route('/user/', methods=['GET', 'POST'])
# def userPage():
#     try:
#         id = request.args.get('id')
#         data = readJSON(DATABASE)
#         if request.method == 'POST':
#             if request.form.get('action1') == 'Voltar':
#                 return redirect(url_for('homeuser', id=id))
            
#         html = htmlHandler()
#         return html.userData(data[id])
#     # return data
#     except:
#         return 'ERROR, user ID is not valid'

# # connection testing
# @app.route('/ping/', methods=['GET', 'POST'])
# def data_handler():
#     # requests data from client
#     received_data = request.args.get('data')
#     data = json.loads(received_data)
    
#     if data:
#         # print data on server screen
#         test = f'{GREEN}TEST SUCCESS{END_COLOR}'
#         print(f'\n\n{BLUE}-------------------------------------------{END_COLOR}\n')
#         time.sleep(1)
#         print(f'{test}. Got connection from {YELLOW}{request.remote_addr}{END_COLOR}. Data sent:')
#         for key in data:
#             print(f'{key}: {YELLOW}{data[key]}{END_COLOR}')
#         print(f'\n{BLUE}-------------------------------------------{END_COLOR}\n\n')
        
#         # write in json database
#         # return redirect(url_for('saveUser', user=dados["Usuário"], new_data=dados))
#         return redirect(url_for('userPage', id=data["Usuário"]))
        
#     else:
#       test = f'{RED}ERROR.{END_COLOR} Couldnt get name'
#       return test

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")

""" flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) """
