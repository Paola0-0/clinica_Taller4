from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'xyzsdfg'

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pao07092002'
app.config['MYSQL_DB'] = 'Clinica'

mysql = MySQL(app)

# -------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------#

# Ruta para la página de inicio de sesión
@app.route('/')

def home():
    return render_template('/index.html')
@app.route('/templates/index.html')

def servicios():
    return render_template('/servicios.html')
@app.route('/templates/servicios.html')

# -------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------#

@app.route('/login.html', methods= ['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = '¡Ingresaste exitosamente!'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Por favor, introduce los datos correctamente'
    return render_template('login.html', mesage = mesage)
    
# -------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------#

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# -------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------#

@app.route('/templates/register.html', methods = ['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Por favor, rellena los datos correctamente'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Por favor, rellena los datos correctamente'
        elif not userName or not password or not email:
            mesage = 'Por favor, rellena los datos solicitados'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = '¡Te has registrado exitosamente!'
    elif request.method == 'POST':
        mesage = 'Por favor, rellena los datos solicitados'
    return render_template('register.html', mesage = mesage)

# -------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')





