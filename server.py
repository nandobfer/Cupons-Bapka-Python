from flask import Flask, escape, request, url_for, redirect, json, render_template
import json, time
from config import *
from functions import *

app = Flask(__name__)

# color constants
RED = '\033[0;31m' 
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
END_COLOR = '\033[0m'

# url
@app.route('/', methods=['GET', 'POST'])
def index():
    # redirecting to another endpoint
    return redirect(url_for('home'))

# home page
@app.route('/home/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form['fname']
        return redirect(url_for('userPage', id=user))
    return render_template("home.html")
    

@app.route('/homeuser/', methods=['GET', 'POST'])
def homeuser():
    # checar se foi passado um id ou não
    id = request.args.get('id')
    if not id:
        return redirect(url_for('home'))

    if request.method == 'POST':
        if request.form.get('action1') == 'Ver dados':
            return redirect(url_for('userPage', id=id))
        elif request.form.get('action2') == 'Sair':
            return redirect(url_for('home'))
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('home_user.html', user = id)
    return render_template("home_user.html", user=id)

# url/argument=name
@app.route('/<name>/')
def hello(name):
    # print on page "Hello, argument passed on URL!"
    return f'<h1>Hello, {escape(name)}!</h1>'

# console printing
# with app.test_request_context():
#     print(url_for('home'))
#     # url_for('functionName', functionArgs = 'args')
#     print(url_for('hello', name='Fernando'))
    
# write at database
@app.route('/save/', methods=['GET', 'POST'])
def saveUser():
    # id = request.args.get('id')
    new_data = json.loads(request.args.get('data'))
    data = readJSON(DATABASE)
    data[new_data['Usuário']] = new_data
    writeJSON(data, DATABASE)
    return '<h1>Success</h1>'

# user page
@app.route('/user/', methods=['GET', 'POST'])
def userPage():
    try:
        id = request.args.get('id')
        data = readJSON(DATABASE)
        if request.method == 'POST':
            if request.form.get('action1') == 'Voltar':
                return redirect(url_for('homeuser', id=id))
            
        html = htmlHandler()
        return html.userData(data[id])
    # return data
    except:
        return 'ERROR, user ID is not valid'

# connection testing
@app.route('/ping/', methods=['GET', 'POST'])
def data_handler():
    # requests data from client
    received_data = request.args.get('data')
    data = json.loads(received_data)
    
    if data:
        # print data on server screen
        test = f'{GREEN}TEST SUCCESS{END_COLOR}'
        print(f'\n\n{BLUE}-------------------------------------------{END_COLOR}\n')
        time.sleep(1)
        print(f'{test}. Got connection from {YELLOW}{request.remote_addr}{END_COLOR}. Data sent:')
        for key in data:
            print(f'{key}: {YELLOW}{data[key]}{END_COLOR}')
        print(f'\n{BLUE}-------------------------------------------{END_COLOR}\n\n')
        
        # write in json database
        # return redirect(url_for('saveUser', user=dados["Usuário"], new_data=dados))
        return redirect(url_for('userPage', id=data["Usuário"]))
        
    else:
      test = f'{RED}ERROR.{END_COLOR} Couldnt get name'
      return test

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="80")

""" flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) """
