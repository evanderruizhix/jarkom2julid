import socket
import threading
import random
import var


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IPaddress = input("Masukkan IP Address: ")
while (IPaddress != var.ipp):
    print("Salah Tolol!!!")
    IPaddress = input("Masukkan IP Address: ")
portnum = int(input("Masukkan Port Number: "))
client.bind((IPaddress, random.randint(8000, 9000)))

password = input("Masukkan password server: ")
while (password != var.password):
    print("Password yang anda masukkan salah!")
    password = input("Masukkan password server: ")

file_name = 'username.csv'
existing_usernames = var.read_usernames(file_name)

name = input("Username: ")
while name in existing_usernames:
    print("Username sudah dipakai!")
    name = input("Username: ")

var.write_username(file_name, name)
print(f"Username '{name}' has been successfully added.")

def receieve():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass
        
thread = threading.Thread(target=receieve)
thread.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), (IPaddress, portnum))

while True:
    message = input("")
    if message == "!q":
        client.sendto(f"Bye {name}!".encode(), (IPaddress, portnum))
        var.delete_username(file_name, name)
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), (IPaddress, portnum))