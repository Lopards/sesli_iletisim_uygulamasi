#  Arayüzlü uygulama için geliştirilen flask uygulaması
#  Rise Together
#  Emirhan Said Erdem
#  Uygulamayı başlatmak için  281. satırdaki Host kısmını kullancağınız serverin veya kendi bilgisayarınızın ip adresini yazınız.

from flask import Flask, render_template, session, redirect, request
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import base64   # Dosya Aktarımı için
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
        #self.setup_routes()
        self.setup_socketio()

    # Get_sid ve  get_active_sids  fonksiyonların amacı sesli mesajın veya yazılı mesajın sadece oda üyelerine göndermektir.
    def get_sid(self, name):
            
            # Bu fonksiyon, verilen ismin sid değerini döndürür
            # Eğer isim self.connected_users sözlüğünde yoksa None döndürür
            for sid, user_data in self.connected_users.items():
                if user_data["name"] == name:
                    return sid
            return None        
    
    def get_active_sids(self, room):
        # Bu fonksiyon, verilen odadaki aktif üyelerin sid değerlerini bir liste olarak döndürür
        # Eğer oda yoksa veya odada aktif üye yoksa boş bir liste döndürür
        active_sids = []
        if room in self.users_in_rooms:
            for name in self.users_in_rooms[room]:
                sid = self.get_sid(name) # Daha önce yazdığımız get_sid fonksiyonunu kullanıyoruz
                if sid:
                    active_sids.append(sid)
        return active_sids

        
    def setup_socketio(self):  
        
        @self.socketio.on("baglan") # Flask' a bağlanan kullanıcıların bilgileri alınıyor ve kaydediliyor.
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
            try:
                file_name = data["file_name"]
                file_data_base64 = data["file_data"]

                # Base64 veriyi çöz
                file_data = base64.b64decode(file_data_base64)

                # Dosyayı kaydet
                with open(file_name, "wb") as file:
                    file.write(file_data)

                print(f"Received file: {file_name}")

                # Base64 ile encode edip geri gönderme işlemi
                with open(file_name, "rb") as file:
                    file_data_encoded = base64.b64encode(file.read()).decode("utf-8")
               
                self.socketio.emit(
                    "file_uploaded", {"file_name": file_name, "file_data": file_data_encoded} 
                )# dosyayı odadakilere gönder

            except Exception as e:
                print(f"Hata dosya alınırken: {e}")

        @self.socketio.on("audio_data") # doktor tarafından fgelen ses verisini odadaki üyelere yönlendirir.
        def audio_data(data1):
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            
            if user_data and user_data["name"] in self.users_in_rooms[room]:
                # Oda içindeki aktif üyelerin sid değerlerini al
                active_sids = self.get_active_sids(room)
                # Mesajı yalnızca aktif üyelere gönder
                for sid in active_sids:
                    emit("data1", data1, to=sid, broadcast=True)
            #emit("data1", data1, to=room, broadcast=True)
     

        @self.socketio.on("audio_data2") # Öğrenci tarafından fgelen ses verisini odadaki üyelere yönlendirir.
        def audio_data2(data2):
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            emit("data2", data2, to=room, broadcast=True)
            #

        @self.socketio.on("output_device_list") # öğrenci bilgisayarının Hoparlör listesi Doktora aktarılınır.
        def output_device_list(List):   
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            emit("liste", List, to=room)

        @self.socketio.on("output_device_index")# Doktor hoparlör listesinden seçtiği indexi gönderir ve hoparlörü seçmiş olur.
        def output_device_list(index):
            user_data = self.connected_users.get(request.sid)
            room = user_data.get("room")
            emit("index", index, to=room)
            #

        @self.socketio.on("message")
        def message(data):
            room = session.get("room") or data["room"]
            sender_name = session.get("name") or data["name"]
            message = data["data"]
            
            efekt = data.get("efekt")
            key = data.get("key")  # Anahtarı al

            if room not in self.rooms:
                print("message!!! ROOM YOK")
                return

            content = {
                "name": sender_name,
                "message": message,
                "efekt": efekt,
                "key": key,  # Anahtarı ekle
            }

            # Odadan çıkartılan kişiyi kontrol et
            user_data = self.connected_users.get(request.sid)
            if user_data and user_data["name"] in self.users_in_rooms[room]:
                # Oda içindeki aktif üyelerin sid değerlerini al
                active_sids = self.get_active_sids(room)
                # Mesajı yalnızca aktif üyelere gönder
                for sid in active_sids:
                    send(content, to=sid)
                self.rooms[room]["messages"].append(content)
                print(f"{sender_name} said: {message}")
            else:
                print(f"{sender_name} odadan çıkartıldığı için mesaj gönderilmedi.")



        @self.socketio.on("see_members_on_room") # Doktorun odadaki üyeleri gormesini sağlar.
        def see_members_on_room():

                user_data = self.connected_users.get(request.sid)
                room = user_data.get("room")
                members = self.rooms[room]["members"]
                emit("members",members,to=room)
        
        @self.socketio.on("remove_member")#Doktorun odadan üye atmasını sağlar
        def remove_member(member_info):
            try:
                user_data = self.connected_users.get(request.sid)
                room = user_data.get("room")
                print(room)

                if member_info in self.rooms[room]["members"]:
                    
                    self.rooms[room]["members"].remove(member_info)
                    print(f"{member_info} odadan çıkartıldı")
                   

                    # Odadan çıkartılan kişiye odadan ayrıldığı bilgisini gönderme
                    self.socketio.emit("user_left", {"name": member_info, "room": room}, to=room)

                if member_info in self.users_in_rooms[room]:
                    self.users_in_rooms[room].remove(member_info)
                    
                    print(f"{member_info} odadaki kullanıcılardan çıkartıldı")
                    

                # Odadan çıkartılan kişinin sid değerini bul
                sid = self.get_sid(member_info)
                # Eğer sid değeri varsa, self.connected_users sözlüğünden sil
                if sid:
  
                    del self.connected_users[sid]
                    
            except Exception as e:
                print("hata:", e)

        


        # ekran görüntüsü paylaşımı için konuldu. Şuan aktif değil.
        @self.socketio.on("start_stream")
        def start_stream():
            print("stream başladı")

        @self.socketio.on("stop_stram") 
        def stop_stram():
            print("stream durdu")      
    
        if __name__ == "__main__":
            self.socketio.run(self.app, host="YOUR_IP_ADRESS", debug=True)


if __name__ == "__main__":
    chat_app = ChatApp()
