from flask import Flask, render_template, request, session, redirect, url_for, send_file
from flask_socketio import join_room, leave_room, send, SocketIO, emit
import random
from string import ascii_uppercase
import base64


app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
app.config["JSON_AS_ASCII"] = False

socketio = SocketIO(app)

rooms = {}
users_in_rooms = {}
room_s = ""  # bu değişkeni eklemeden önce ses verileri bütün odalara gidityordu. artık sesler kullanıcının olduğu odaya gidecek.


def generate_unique_code(length):  # Benzersiz oda kodu oluşturmaya yarar
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


@app.route(
    "/", methods=["POST", "GET"]
)  # Eğer talep bir "POST" talebi ise, kullanıcının girdiği isim (name) ve oda kodu (code) bilgilerini alır.
def home():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template(
                "home.html", error="Please enter a name.", code=code, name=name
            )

        if join != False and not code:
            return render_template(
                "home.html", error="Please enter a room code.", code=code, name=name
            )

        room = code
        if create != False:
            room = generate_unique_code(5)
            rooms[room] = {"members": [name], "messages": []}
            users_in_rooms[room] = [name]
        elif code not in rooms:
            return render_template(
                "home.html", error="Room does not exist.", code=code, name=name
            )
        """else:
            rooms[room]["members"].append(name)
            users_in_rooms[room].append(name)"""

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")


@app.route("/room", methods=["GET", "POST"])
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):  # Kullanıcıların sohbet odasında mesaj göndermesini sağlar
    room = session.get("room") or data["room"]
    name = session.get("name") or data["name"]
    message = data["data"]

    efekt = data.get("efekt")
    key = data.get("key")  # Anahtarı al

    if room not in rooms:
        return

    content = {
        "name": name,
        "message": message,
        "efekt": efekt,
        "key": key,  # Anahtarı ekle
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{name} said: {message}")


@socketio.on("connect")
def connect(
    auth,
):  # Kullanıcıların sohbet odasına bağlanmasını sağlayar aut = kimlik bilgileri
    print(auth)
    if (
        not auth
    ):  # ğer auth bilgisi yoksa veya eksikse, "Auth verisi eksik veya hatalı." şeklinde bir hata mesajı yazdırır ve fonksiyondan çıkar.
        print("Auth verisi eksik veya hatalı.")
        return

    name = auth.get("name")  # Name ve room bilgilerini auth içinden alır
    room = auth.get("room")

    if not room or not name:
        print("room yok veya name yok")
        return
    if room not in rooms:  # eğer alınan room kodu rooms içinde yoksa fonksiyondan çıkar
        print("room yok")
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"].append(name)
    users_in_rooms[room].append(name)
    print(f"{name} joined room {room}")


def disconnect():
    room = session.get("room")
    name = session.get("name")

    if room in rooms:
        rooms[room]["members"].remove(name)
        users_in_rooms[room].remove(name)
        if len(rooms[room]["members"]) <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@socketio.on("create_room")
def handle_create_room(
    data,
):  # kullanıcıların oda oluşturmasını sağlar .data içined oda sahibi ismi(name) ve oda kodu vardır
    name = data["name"]
    code = data["code"]
    global room_s
    room_s = code  # sesin hangi odaya gideceği belirlendi

    if code not in rooms:
        rooms[code] = {"members": [name], "messages": []}
        users_in_rooms[code] = [name]
        print(f"Oda oluşturuldu. Adı: {name}, Kodu: {code}")
    else:
        print("Bu oda kodu zaten kullanılıyor.")
    join_room(room_s)  # odaya katılındı

    send("message", {"name": name, "code": code}, room=request.sid)


@socketio.on("take_rooms")  # oda bilgilerini paylaşmak için konuldu, şu anda kullanılmıyor
def take_rooms():
    for room_name, room_data in rooms.items():
        members = room_data["members"]
        print(f"Üyeleri: {', '.join(members)}")
        emit("members_data", members)


@socketio.on("file_upload")
def handle_file_upload(data):# doktor tarafından öğrenci tarafına dosya paylaşımı yapar. (Öğrenci tarafında sıkıntı olabilir tekrar bak)
    file_name = data["file_name"]
    file_data_base64 = data["file_data"]

    # Base64 veriyi çöz
    file_data = base64.b64decode(file_data_base64)

    # Dosyayı kaydet
    with open(file_name, "wb") as file:
        file.write(file_data)
    file_data_encoded = base64.b64encode(file_data).decode("utf-8")
    print(f"Received file: {file_name}")
    socketio.emit(
        "file_uploaded", {"filename": file_name, "file_data": file_data_encoded}
    )


@socketio.on("audio_data") #ses iletişimi için; doktor tarafından öğrenciye
def audio_data(data1):
    emit("data1", data1, to=room_s, broadcast=True)


@socketio.on("audio_data2")  #ses iletişimi için; öğrenci tarafından doktora
def audio_data2(data2):
    emit("data2", data2, to=room_s, broadcast=True)


@socketio.on("output_device_list") # hoparlör listesini öğrenci tarafından doktor tarafına göndermek için
def output_device_list(List):
    emit("liste", List, to=room_s)

@socketio.on("output_device_index") # öğrenci pc 'nin indexini gönderen metod
def output_device_list(index):
    emit("index", index, to=room_s)

@socketio.on("screenShot")  # ekran görüntüsünü paylaşmak için, şu anda aktif değil.
def screenShot(screenShot):
    room = session.get("room")
    print("ekran görüntüsü geldi")
    emit("screenShot", screenShot, to=room)  # emit ile paylaş

    print("ekran görüntüsü gönderildi")


if __name__ == "__main__":
    socketio.run(app, host="YOUR_IP_ADRESS", debug=True)
