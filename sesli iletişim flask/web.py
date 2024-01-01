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
        ] = "filesystem"  #
        Session(self.app)

        self.rooms = {}
        self.users_in_rooms = {}

        self.connected_users= {}
        self.setup_routes()
        self.setup_socketio()

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")
        
        
    def setup_socketio(self):  
        @self.socketio.on("baglan")
        def baglan(data):
            print("veri:",data)
            name = data.get("name")  # Name ve room bilgilerini auth içinden alır
            room = data.get("room")
            print("name print ediliyor:",name,room)

            if not room or not name:
                print("room yok veya name yok")
                return
            if room not in self.rooms:  # eğer alınan room kodu rooms içinde yoksa fonksiyondan çıkar
                print("room yok")
                leave_room(room)
                return
            
            
            join_room(room)
            
            send({"name": name, "message": "has entered the room"})
            self.rooms[room]["members"].append(name)
            self.users_in_rooms[room].append(name)
            print("self.users.in.room [room]pritn etmek ben",self.users_in_rooms[room])
            self.connected_users[request.sid] = {"name": name, "room": room} # Bağlı kullanıcıların bilgilerini sakla
            print(f"{name} joined room {room}")


        @self.socketio.on("connect")
        def connect(auth):  # Kullanıcıların sohbet odasına bağlanmasını sağlayar aut = kimlik bilgileri
            print("baglanıldi")
            


        @self.socketio.on("disconnect") # odadan çıkan üyeleri odadan siler, eğer odadaki üye sayısı 0 ise odayı del yapar.
        def disconnect():
            print("Kullanıcı odadan çıkıverdi: {}".format(request.sid))
            user_data = self.connected_users.get(request.sid)
            
            # request.sid'ye bağlı olan kullanıcının bilgilerini al
            if user_data:
                name = user_data.get("name")
                room = user_data.get("room")
                print(name,room, "odadan çıktı")

                if room in self.rooms:
                    self.rooms[room]["members"].remove(name)
                    self.users_in_rooms[room].remove(name)
                    print(len(self.users_in_rooms[room]))
                    print(self.rooms[room])
                    if room in self.rooms and len(self.rooms[room]["members"]) <= 0:
                        
                        del self.rooms[room]
                        print("aktif odalar",self.rooms)

                    self.socketio.emit("user_left", {"name": name, "room": room}, to=room)
                    print(f"{name} has left the room {room}")



        @self.socketio.on("create_room")
        def handle_create_room(data): # kullanıcıların oda oluşturmasını sağlar .data içined oda sahibi ismi(name) ve oda kodu vardır
  
            name = data["name"]
            code = data["room"]

            if code not in self.rooms:
                self.rooms[code] = {"members": [name], "messages": []}
                
                self.users_in_rooms[code] = [name]
                print(self.users_in_rooms[code],"odaya eklendi CREATE ROOM")
                print(f"Oda oluşturuldu. Adı: {name}, Kodu: {code}")
            elif code in self.rooms:
                print("Bu oda kodu zaten kullanılıyor.")

            join_room(code)  # odaya katılındı

            self.connected_users[request.sid] = {"name": name, "room": code}
            self.socketio.emit("create_room", {"name": name, "room": code}, to=code)




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
         

        @self.socketio.on("audio_data") # doktor tarafından fgelen ses verisini odadaki üyelere yönlendirir.
        def audio_data(data1):
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            emit("data1", data1, to=room, broadcast=True)
     

        @self.socketio.on("audio_data2") # Öğrenci tarafından fgelen ses verisini odadaki üyelere yönlendirir.
        def audio_data2(data2):
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            emit("data2", data2, to=room, broadcast=True)
            #

        @self.socketio.on("output_device_list")
        def output_device_list(List):   
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            emit("liste", List, to=room)

        @self.socketio.on("output_device_index")
        def output_device_list(index):
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            emit("index", index, to=room)
            #

        @self.socketio.on("message")
        def message(data):
            room = session.get("room") or data["room"]
            name = session.get("name") or data["name"]
            message = data["data"]
            print("message metodu name ve room print:",name,room)
            efekt = data.get("efekt")
            key = data.get("key")  # Anahtarı al

            if room not in self.rooms:
                print("message!!! ROOM YOK")
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

        @self.socketio.on("see_members_on_room")
        def see_members_on_room():
                #room = session.get("room") or data["room"]
                
                user_data = self.connected_users.get(request.sid)
                room = user_data.get("room")
                members = self.rooms[room]["members"]
                emit("members",members,to=room)
        
        @self.socketio.on("remove_member")
        def remove_member(member_info):
            try:
                user_data = self.connected_users.get(request.sid)
                room = user_data.get("room")

                self.users_in_rooms[room].remove(member_info)

            except Exception as e:
                print("hata,", e)

    
        if __name__ == "__main__":
            self.socketio.run(self.app, host="192.168.1.45", debug=True)


if __name__ == "__main__":
    chat_app = ChatApp()
