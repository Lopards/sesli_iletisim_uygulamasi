from flask import Flask, render_template, session, redirect, request
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import base64
from flask_session import Session


class ChatApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "hjhjsdahhds"
        self.app.config["JSON_AS_ASCII"] = False
        self.socketio = SocketIO(self.app)
        # Flask-Session konfigürasyonu
        self.app.config[
            "SESSION_TYPE"
        ] = "filesystem"  # Örnek bir depolama tipi, siz kendi projenize uygun birini seçebilirsiniz
        Session(self.app)

        self.rooms = {}
        self.users_in_rooms = {}
        self.room_s = {}
        self.connected_users= {}
        self.setup_routes()


    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")
        
        @self.socketio.on("baglan")
        def baglan(data):
            print("veri:",data)
            name = data.get("name")  # Name ve room bilgilerini auth içinden alır
            room = data.get("room")
            print("name print ediliyor:",name)

            if not room or not name:
                print("room yok veya name yok")
                return
            if room not in self.rooms:  # eğer alınan room kodu rooms içinde yoksa fonksiyondan çıkar
                print("room yok")
                leave_room(room)
                return
            
            join_room(room)
            
            # Bağlı kullanıcıların bilgilerini sakla
            


            send({"name": name, "message": "has entered the room"})
            self.rooms[room]["members"].append(name)
            self.users_in_rooms[room].append(name)
            print("self.users.in.room [room]pritn etmek ben",self.users_in_rooms[room])
            print(f"{name} joined room {room}")


        @self.socketio.on("connect")
        def connect(auth):  # Kullanıcıların sohbet odasına bağlanmasını sağlayar aut = kimlik bilgileri
            print("baglanıldi")
            


        @self.socketio.on("disconnect")
        def disconnect():
            print("Kullanıcı odadan çıkıverdi: {}".format(request.sid))
            user_data = self.connected_users.get(request.sid)
            print("disccenet tarafı",user_data.get("name"))
            # request.sid'ye bağlı olan kullanıcının bilgilerini al
            if user_data:
                name = user_data.get("name")
                room = user_data.get("room")
                print(name, "odadan çıktı")

                if room in self.rooms:
                    self.rooms[room]["members"].remove(name)
                    self.users_in_rooms[room].remove(name)
                    print(len(self.users_in_rooms[room]))
                    if room in self.rooms and len(self.rooms[room]["members"]) <= 0:
                        del self.rooms[room]

                    self.socketio.emit("user_left", {"name": name, "room": room}, to=room)
                    print(f"{name} has left the room {room}")



        @self.socketio.on("create_room")
        def handle_create_room(data):
  
            name = data["name"]
            code = data["code"]

            if code not in self.rooms:
                self.rooms[code] = {"members": [name], "messages": []}
                self.users_in_rooms[code] = [name]
                print(self.users_in_rooms[code],"123")
                print(f"Oda oluşturuldu. Adı: {name}, Kodu: {code}")
            elif code in self.rooms:
                print("Bu oda kodu zaten kullanılıyor.")

            join_room(code)  # odaya katılındı

            self.connected_users[request.sid] = {"name": name, "room": code}
            self.socketio.emit("create_room", {"name": name, "code": code}, to=code)




        @self.socketio.on("file_upload")
        def handle_file_upload(data):
            file_name = data["file_name"]
            file_data_base64 = data["file_data"]

            # Base64 veriyi çöz
            file_data = base64.b64decode(file_data_base64)

            # Dosyayı kaydet
            with open(file_name, "wb") as file:
                file.write(file_data)
            file_data_encoded = base64.b64encode(file_data).decode("utf-8")
            print(f"Received file: {file_name}")
            self.socketio.emit(
                "file_uploaded", {"filename": file_name, "file_data": file_data_encoded}
            )
            # (Kodunuzun geri kalanı burada)

        @self.socketio.on("audio_data")
        def audio_data(data1):
            emit("data1", data1, to=self.room_s, broadcast=True)
            # (Kodunuzun geri kalanı burada)

        @self.socketio.on("audio_data2")
        def audio_data2(data2):
            emit("data2", data2, to=self.room_s, broadcast=True)
            # (Kodunuzun geri kalanı burada)

        @self.socketio.on("output_device_list")
        def output_device_list(List):
            print(self.users_in_rooms)
            print(self.rooms)
            print(self.room_s,"room_s")
            emit("liste", List, to=self.room_s)

        @self.socketio.on("output_device_index")
        def output_device_list(index):
            emit("index", index, to=self.room_s)
            # (Kodunuzun geri kalanı burada)

        @self.socketio.on("message")
        def message(data):
            room = session.get("room") or data["room"]
            name = session.get("name") or data["name"]
            message = data["data"]

            efekt = data.get("efekt")
            key = data.get("key")  # Anahtarı al

            if room not in self.rooms:
                print("heyo")
                return

            content = {
                "name": name,
                "message": message,
                "efekt": efekt,
                "key": key,  # Anahtarı ekle
            }
            send(content, to=room)
            self.rooms[room]["messages"].append(content)
            print(f"{name} said: {message}")




        if __name__ == "__main__":
            self.socketio.run(self.app, host="192.168.1.45", debug=True)


if __name__ == "__main__":
    chat_app = ChatApp()
