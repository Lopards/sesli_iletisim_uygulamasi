from flask import Flask, render_template, request,session,redirect,url_for
from flask_mysqldb import MySQL
import hashlib
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# MySQL veritabanı bağlantı ayarları
app.config['MYSQL_HOST'] = 'awsveri.cwguyhuwi5xu.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'rise'
app.config['MYSQL_PASSWORD'] = 'Osmaniye12!'
app.config['MYSQL_DB'] = 'kullanici_veri'

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

        current_time = datetime.now()
        sifre_degisim_tarihi = current_time
        bir_hafta_sonrasi = sifre_degisim_tarihi + timedelta(days=7)
        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO veriler (kullanici_ad, sifre, salt, giris_tarihi, sifre_degisim_tarihi) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sorgu, (name, password, hashed_password, current_time, bir_hafta_sonrasi))
        mysql.connection.commit()
        cursor.close()
        kayit_basarili = True  # Kayıt başarılı oldu
        return render_template("login.html", kullanici_ad=name ,kayit_basarili=kayit_basarili)
    else:
        return render_template("register.html")

@app.route('/login.html', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM veriler WHERE kullanici_ad = %s', (username,))
        account = cursor.fetchone()
        cursor.close()

        if account:
            giris_tarihi = account['giris_tarihi']
            sifre_degisim_tarihi = account['sifre_degisim_tarihi']
            bir_hafta_sonrasi = sifre_degisim_tarihi + timedelta(days=7)

            if bir_hafta_sonrasi <= datetime.now():
                # Şifre sıfırlama işlemine yönlendir
                return redirect(url_for('sifre_sifirlama'))

            stored_salt = account['salt']
            stored_password = account['sifre']
            input_salted_password = stored_salt + password.encode('utf-8')
            input_hashed_password = hashlib.sha256(input_salted_password).hexdigest()

            if input_hashed_password == stored_password:
                # Kullanıcı şifresi doğru
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['kullanici_ad']
                msg = 'Logged in successfully !'
                return render_template('index.html', msg=msg)
            else:
                msg = 'Incorrect username / password !'
        else:
            msg = 'User not found !'

    return render_template('login.html', msg=msg)

@app.route('/sifre_sifirlama', methods=['GET', 'POST'])
def sifre_sifirlama():
    if request.method == 'POST':
        yeni_sifre = request.form.get('yeni_sifre')

        # Yeni şifreyi tuzla ve hashle
        salt = os.urandom(16)
        salted_password = salt + yeni_sifre.encode('utf-8')
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        user_id = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE veriler SET sifre = %s, salt = %s, sifre_degisim_tarihi = %s WHERE id = %s',
                       (hashed_password, salt, datetime.now(), user_id))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('index'))

    return render_template('sifre_sifirlama.html')

if __name__ =="__main__":
    app.run(debug = True)