from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import hashlib
import os
from datetime import datetime, timedelta
import random
import string
from email.mime.text import MIMEText
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
app = Flask(__name__)
app.config["MYSQL_HOST"] = "rise.czfoe4l74xhi.eu-central-1.rds.amazonaws.com"
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "Osmaniye12!"
app.config["MYSQL_DB"] = "rise_data"


mysql = MySQL(app)
email_ = ""



@app.route("/")
def index():
    return render_template("index.html")
@app.route("/index.html")
def anasayfa():
    return render_template("index.html")
@app.route("/about.html")
def about():
    return render_template("about.html")

def send_verification_email(email, verification_code):
        # Outlook SMTP sunucu ve bağlantı bilgileri
        try:






            msg = verification_code
            subj = "Doğrulama Kodu"
            content = "Subject: {} \n\n{}".format(subj, msg)

            mail_address = "emirhanerdem353580@gmail.com"
            password = "mnzt bepc qxfz xwcd"
            sent_to = email

            mail = SMTP("smtp.gmail.com", 587)
            mail.ehlo()  # maile bağlan
            mail.starttls()  # mesajı şifrele

            # login işlemi
            mail.login(mail_address, password)

            # e-postayı gönder
            mail.sendmail(mail_address, sent_to, content.encode("utf-8"))
            print("E-posta gönderildi")

            # bağlantıyı kapat
            mail.quit()
            return True
        except Exception as e:
            print("hata:",e)

def generate_verification_code():
    code_length = 6
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(code_length))


@app.route("/register.html", methods=["GET", "POST"])
def register():
    kayit_basarili = False
    kayit_var = False

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        global email_
        email_ = email

        sorgu = "SELECT * FROM veriler WHERE kullanici_ad = %s OR email = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu, (name, email))
        kayit = cursor.fetchone()

        if kayit:
            kayit_var = True
            return render_template("register.html", kayit_var=kayit_var)
        else:
            salt = os.urandom(16)
            salted_password = salt + password.encode("utf-8")
            hashed_password = hashlib.sha256(salted_password).hexdigest()
            print(hashed_password)
            print(salt)
            current_time = datetime.now()
            sifre_degisim_tarihi = current_time + timedelta(days=7)

            verification_code = generate_verification_code()

            if send_verification_email(email, verification_code):
                cursor = mysql.connection.cursor()
                sorgu = "INSERT INTO veriler (kullanici_ad, sifre, email, salt, verification_code, verified, giris_tarihi, sifre_degisim_tarihi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    sorgu,
                    (
                        name,
                        hashed_password,
                        email,
                        salt,
                        verification_code,
                        False,
                        current_time,
                        sifre_degisim_tarihi,
                    ),
                )
                mysql.connection.commit()
                kayit_basarili = True

        cursor.close()

        return render_template("verify_email.html")

    else:
        return render_template("register.html", kayit_var=kayit_var)

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM veriler WHERE kullanici_ad = %s", (username,))
        account = cursor.fetchone()
        cursor.close()

        if account:
            giris_tarihi = account["giris_tarihi"]
            sifre_degisim_tarihi = account["sifre_degisim_tarihi"]
            bir_hafta_sonrasi = sifre_degisim_tarihi + timedelta(days=7)

            if bir_hafta_sonrasi <= datetime.now():
                return redirect(url_for("sifre_sifirlama"))

            stored_salt = account["salt"]
            stored_password = account["sifre"]
            input_salted_password = stored_salt + password.encode("utf-8")
            input_hashed_password = hashlib.sha256(
                input_salted_password
            ).hexdigest()

            if input_hashed_password == stored_password:
                session["loggedin"] = True
                session["id"] = account["id"]
                session["username"] = account["kullanici_ad"]
                msg = "Logged in successfully!"
                return render_template("index.html", msg=msg)
            else:
                msg = "Incorrect username/password!"
        else:
            msg = "User not found!"

    return render_template("login.html", msg=msg)

@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    if request.method == "POST":
        verification_code = request.form.get("verification_code")

        global email_

        cursor = mysql.connection.cursor()
        sorgu = "SELECT verification_code FROM veriler WHERE email = %s"
        cursor.execute(sorgu, (email_,))
        verification_code_db = cursor.fetchone()

        if verification_code_db and verification_code == verification_code_db[0]:
            cursor.execute(
                "UPDATE veriler SET verified = 1 WHERE verification_code = %s",
                (verification_code_db[0],),
            )

            mysql.connection.commit()

            msg = "E-posta adresiniz başarıyla doğrulandı!"
            return render_template("index.html", msg=msg)
        else:
            msg = "Geçersiz doğrulama kodu!"
            return render_template(
                "verify_email.html", verification_error=True, msg=msg
            )
    return render_template("verify_email.html")

if __name__ == "__main__":
    
    
    app.run(debug=True)
