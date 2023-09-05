from flask import Flask, render_template, request,session
from flask_mysqldb import MySQL
import hashlib
import os
from datetime import datetime

app = Flask(__name__)

# MySQL veritabanı bağlantı ayarları
app.config['MYSQL_HOST'] = 'emirhan.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'emirhan'
app.config['MYSQL_PASSWORD'] = 'XXX'
app.config['MYSQL_DB'] = 'emirhan$default'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def anasayfa():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        # Tuz oluştur
        salt = os.urandom(16)

        # Şifre ile tuzu birleştir
        salted_password = salt + password.encode('utf-8')

        # Hashleme işlemi
        hashed_password = hashlib.sha256(salted_password).hexdigest()


        current_time = datetime.now() #kayit zamanı için
        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO veriler VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu, (name, password,hashed_password,current_time))
        mysql.connection.commit()
        cursor.close()
        kayit_basarili = True  # Kayıt başarılı oldu
        return render_template("login.html", kullanici_ad=name, sifre=password,kayit_basarili=kayit_basarili)
    else:
        return render_template("register.html")

@app.route('/login.html', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM veriler WHERE kullanici_ad = % s AND sifre = % s', (username, password ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('login.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
            return render_template('index.html', msg = msg)

    else:
        return render_template('index.html', msg = msg)
