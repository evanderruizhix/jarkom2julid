import socket
import threading
import var

import client_GUI  #Import GUI agar GUI pada client dapat dijalankan hanya dengan satu kali run
if __name__ == "__main__":
    client_GUI.run_gui()


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Implementasi UDP

IPaddress = input("Masukkan IP Address: ")
while (IPaddress != var.IPAddress): # Pengecekan IP Address
    print("IP Address yang dimasukkan tidak sesuai!")
    IPaddress = input("Masukkan IP Address: ")

portnum = int(input("Masukkan Port Number: "))

password = input("Masukkan password server: ") # Pengecekan password
while (password != var.password):
    print("Password yang anda masukkan salah!")
    password = input("Masukkan password server: ")

# Variabel file .csv
file_name = 'username.csv'
file_name_message = 'messages.csv'

# Pengecekan input username
existing_usernames = var.read_usernames(file_name)
name = input("Username: ")
while name in existing_usernames: # Jika username sudah ada pada csv, maka akan meminta input lagi
    print("Username sudah dipakai!")
    name = input("Username: ")

var.write_username(file_name, name) # Penulisan username ke username.csv jika username tersedia


# Fungsi agar client dapat menerima broadcast dari server
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass
        
thread = threading.Thread(target=receive)
thread.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), (IPaddress, portnum)) # Mengirim username ke server saat join

while True:
    message = input("")
    if message == "!q": # Command untuk keluar dari chatroom
        client.sendto(f"Bye {name}!".encode(), (IPaddress, portnum))
        var.delete_username(file_name, name)
        exit()
    else: # Penulisan message ke chatroom, untuk dikirim ke server
        client.sendto(f"{name}: {message}".encode(), (IPaddress, portnum))