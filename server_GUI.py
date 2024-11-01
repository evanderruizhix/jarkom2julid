import socket
import threading
import queue
import tkinter as tk
from tkinter import scrolledtext

messages = queue.Queue()
clients = {}
client_names = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Implementasi UDP
hostname = socket.gethostname()
sIPaddress = socket.gethostbyname(hostname) # Mendapatkan IP address dari server
print(sIPaddress)
server.bind((sIPaddress, 9002))

# Tampilan GUI server
class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Chatroom")
        
        # Tampilan untuk teks message yang diterima server
        self.chat_display = scrolledtext.ScrolledText(self.root, height=20, width=60, state=tk.DISABLED)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10)

        # Pesan ketika server dinyalakan
        self.log_message("Server berhasil dinyalakan!")

        t1 = threading.Thread(target=self.receive)
        t2 = threading.Thread(target=self.broadcast)

        t1.start()
        t2.start()

    def log_message(self, message):
        """Display chat log"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def receive(self):
        """Penerimaan pesan dari client"""
        while True:
            try:
                message, addr = server.recvfrom(1024)
                messages.put((message, addr))
            except:
                pass

    def broadcast(self):
        """Pengiriman broadcast ke client"""
        while True:
            while not messages.empty():
                message, addr = messages.get()
                decoded_message = message.decode()

                if addr not in clients:
                    clients[addr] = addr
                if decoded_message.startswith("SIGNUP_TAG:"):
                    name = decoded_message.split(":")[1]
                    client_names[addr] = name
                    self.log_message(f"{name} berhasil memasuki chatroom!")
                elif decoded_message == "!q":
                    # Ketika client keluar dari chatroom, menampilkan sebuah pesan
                    name = client_names.get(addr, "Unknown")
                    self.log_message(f"{name} telah keluar dari chatroom.")
                    clients.pop(addr, None)
                    client_names.pop(addr, None)
                else: # Menampilkan dan mengirimkan pesan lainnya ke server
                    self.log_message(f"{decoded_message}")
                    for client in clients:
                        try:
                            server.sendto(message, client)
                        except:
                            clients.pop(client)

# Fungsi untuk menjalankan GUI
def run_server_gui():
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_server_gui()
