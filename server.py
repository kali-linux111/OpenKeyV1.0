import socketserver
import threading
import json
import random

class handler():
    def save(self):
        with lock:
            json.dump(user_config,open('user_config.json','w'))
            json.dump(id_table,open('id_table.json','w')) 

    def radmon_str(size:int):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k=size))

    def login(user:str,password:str):
        if user in user_config:
            if user_config[user]["password"]==password:
                return True
            else:
                return False
        else:
            return False

    def register(user:str,password:str):
        with lock:
            if user in user_config:
                return False
            else:
                user_config[user]={}
                user_config[user]["password"]=password
                user_config[user]["id"]="Unbind"
                handler().save()
                return True
    
    def query_user(user:str):
        if user in user_config:
            return user_config[user]
        else:
            return None

    def query_id(id:str):
        if id in id_table:
            return id_table[id]
        else:
            return None

    def bind_id(id:str,user:str):
        with lock:
            if id in id_table:
                if id_table[id]["user"]=="Unbind":
                    id_table[id]["user"]=user
                    user_config[user]["id"]=id
                    handler().save()
                    return True
                else:
                    return False
            else:
                return False

    def add_id(name:str,telephone:str,email:str):
        global id_table, lock
        with lock:
            id=handler.radmon_str(16)
            id_table[id] = {}
            id_table[id]["name"]=name
            id_table[id]["telephone"]=telephone
            id_table[id]["email"]=email 
            id_table[id]["user"]="Unbind"
            handler().save()
        return id

class MyTCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        username=None
        while True:
            data=self.request.recv(1024).decode('utf-8')
            try:
                msg=json.loads(data)
            except:
                self.request.send(json.dumps({"code":-1,"msg":"Invalid message format"}).encode())
                continue
            if msg["type"]=="login":
                if handler.login(msg["user"],msg["password"]):
                    username=msg["user"]
                    self.request.send(json.dumps({"code":0,"msg":"Login success"}).encode())
                else:
                    self.request.send(json.dumps({"code":-1,"msg":"Login failed"}).encode())
            elif msg["type"]=="register":
                if handler.register(msg["user"],msg["password"]):
                    username=msg["user"]
                    self.request.send(json.dumps({"code":0,"msg":"Register success"}).encode()) 
                else:
                    self.request.send(json.dumps({"code":-1,"msg":"Register failed"}).encode())
            elif msg["type"]=="query_user":
                if username==None:
                    self.request.send(json.dumps({"code":-1,"msg":"Please login first"}).encode())
                else:
                    profile=handler.query_user(username)
                    if profile==None:
                        self.request.send(json.dumps({"code":-1,"msg":"System fault"}).encode())
                    else:
                        self.request.send(json.dumps({"code":0,"msg":"Query success","password":profile["password"],"bind_id":profile["id"]}).encode())
            elif msg["type"]=="query_id":
                profile=handler.query_id(msg["id"])
                if profile==None:
                    self.request.send(json.dumps({"code":-1,"msg":"ID not found"}).encode())
                else:
                    self.request.send(json.dumps({"code":0,"msg":"Query success","name":profile["name"],"telephone":profile["telephone"],"email":profile["email"],"bind_user":profile["user"]}).encode())

            elif msg["type"]=="bind_id":
                if username==None:
                    self.request.send(json.dumps({"code":-1,"msg":"Please login first"}).encode())
                else:
                    if handler.bind_id(msg["id"],username):
                        self.request.send(json.dumps({"code":0,"msg":"Bind success"}).encode())
                    else:
                        self.request.send(json.dumps({"code":-1,"msg":"Bind failed"}).encode())

class MyThread(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

class MyAPP():
    def main():
        print("Welcom to OpenKey V1.0 Server")
        print("Reading configs......")
        try:
            global user_config
            user_config=json.load(open('user_config.json','r'))
        except:
            user_config={}
            print("Configs not found, creating new configs")
            open('user_config.json','w').close()
            handler().save()
        try:
            global id_table
            id_table=json.load(open('id_table.json','r'))
        except:
            id_table={}
            print("Configs not found, creating new configs")
            open('id_table.json','w').close()
            handler().save()
        print("Configs readed")
        global lock
        lock=threading.RLock()
        server=MyThread(("127.0.0.1",8000),MyTCPServer)
        server_thread=threading.Thread(target=server.serve_forever)
        server_thread.daemon=True
        server_thread.start()
        print("Server started")
        while True:
            print("Type \"add_id\" to add a new ID")
            s=input(">")
            if s=="add_id":
                name=input("Name:")
                telephone=input("Telephone:")
                email=input("Email:")
                id=handler.add_id(name,telephone,email)
                print("ID added:",id)

if __name__=="__main__":
    MyAPP.main()