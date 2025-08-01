import socket
import json

class MyClient():
    def main():
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(('localhost',8000))
        username="Unlogin"
        while True:
            s=input("("+username+")>")
            if s=="login":
                username=input("Username:")
                password=input("Password:")
                client.send(json.dumps({"type":"login","user":username,"password":password}).encode())
                data=client.recv(1024).decode()
                try:
                    msg=json.loads(data)
                except:
                    print("System fault")
                    continue
                if msg["code"]==0:
                    username=username
                    print("Login success")
                else:
                    print("Login failed")
            elif s=="register":
                username=input("Username:")
                password=input("Password:")
                client.send(json.dumps({"type":"register","user":username,"password":password}).encode())
                data=client.recv(1024).decode()
                try:
                    msg=json.loads(data)
                except:
                    print("System fault")
                    continue
                if msg["code"]==0:
                    username=msg["user"]
                    print("Register success")
                else:
                    print("Register failed")

            elif s=="query_user":
                client.send(json.dumps({"type":"query_user"}).encode())
                data=client.recv(1024).decode()
                try:
                    msg=json.loads(data)
                except:
                    print("System fault")
                    continue
                if msg["code"]==0:
                    print("User:",username,"Password:",msg["password"],"Bind ID:",msg["bind_id"])
                else:
                    print("Query failed")

            elif s=="query_id":
                id=input("ID:")
                client.send(json.dumps({"type":"query_id","id":id}).encode())
                data=client.recv(1024).decode()
                try:
                    msg=json.loads(data)
                except:
                    print("System fault")
                    continue
                if msg["code"]==0:
                    print("Name:",msg["name"],"Telephone:",msg["telephone"],"Email:",msg["email"],"Bind User:",msg["bind_user"])
                else:
                    print("Query failed")

            elif s=="bind_id":
                id=input("ID:")
                client.send(json.dumps({"type":"bind_id","id":id}).encode())
                data=client.recv(1024).decode()
                try:
                    msg=json.loads(data)
                except:
                    print("System fault")
                    continue
                if msg["code"]==0:
                    print("Bind success")
                else:
                    print("Bind failed")

            elif s=="exit":
                client.send(json.dumps({"type":"exit"}).encode())
                break
            else:
                print("Invalid command")


if __name__=="__main__":
    MyClient.main()