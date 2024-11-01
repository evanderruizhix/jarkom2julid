import socket
import threading
import queue

import server_GUI #Import GUI agar GUI pada server dapat dijalankan hanya dengan satu kali run
if __name__ == "__main__":
    server_GUI.run_server_gui()

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Implementasi UDP
hostname = socket.gethostname()
sIPaddress = socket.gethostbyname(hostname) # Mendapatkan IP address dari server
print(sIPaddress) # Print di sini digunakan hanya untuk memudahkan pengguna dalam mendapatkan IP address dari server
server.bind((sIPaddress, 9002)) # Port 9002 karena memanfaatkan Hamachi

# Fungsi server supaya dapat menerima messages dari client
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

# Fungsi server untuk menampilkan dan mengirim pesan client ke client lainnya
def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"): # Saat client baru memasuki chatroom
                        name = message.decode()[message.decode().index(":")+1:]
                        print(f"{name} berhasil memasuki chatroom!")
                    else: # Pengiriman pesan ke client
                        server.sendto(message, client)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()