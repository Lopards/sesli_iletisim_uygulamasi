from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL veritabanı bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Osmaniye12!",
    database="rise_together"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def anasayfa():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/register.html')
def register_page():
    return render_template("register.html")



@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Verileri MySQL veritabanına ekleme
    query = "INSERT INTO kullanici_verileri (kullanici_ad, kullanici_sifre, kayit_zamani) VALUES (%s, %s, %s)"
    values = (name, email, password)
    cursor.execute(query, values)
    db.commit()

    return "Kayıt başarıyla tamamlandı!"

"""if __name__ == '__main__':
    app.run(debug=True)"""
