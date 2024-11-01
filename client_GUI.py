import socket
import threading
import tkinter as tk
from tkinter import messagebox
import var

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Implementasi UDP

# Variabel file .csv
file_name = 'username.csv'
existing_usernames = var.read_usernames(file_name)

# Tampilan GUI client
class ChatroomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatroom App")

        self.IPaddress = None
        self.portnum = None
        self.password = None
        self.name = None

        self.create_ip_port_popup() # Memulai dari pop-up pengisian IP dan portnum

    def create_ip_port_popup(self):
        """Pop-up untuk pengisian IP address dan Port number yang akan digunakan"""
        self.ip_port_popup = tk.Toplevel(self.root)
        self.ip_port_popup.title("Enter IP Address and Port Number")
        
        tk.Label(self.ip_port_popup, text="IP Address:").grid(row=0, column=0)
        self.ip_entry = tk.Entry(self.ip_port_popup)
        self.ip_entry.grid(row=0, column=1)

        tk.Label(self.ip_port_popup, text="Port Number:").grid(row=1, column=0)
        self.port_entry = tk.Entry(self.ip_port_popup)
        self.port_entry.grid(row=1, column=1)

        submit_btn = tk.Button(self.ip_port_popup, text="Submit", command=self.submit_ip_port)
        submit_btn.grid(row=2, columnspan=2)

    def submit_ip_port(self):
        """Validasi IP address dan Port number"""
        self.IPaddress = self.ip_entry.get()
        try:
            self.portnum = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Port number harus berupa angka!") # Jika input portnum bukan angka
            return

        # Jika IP dan portnum valid
        if self.IPaddress == var.IPAddress:
            self.ip_port_popup.destroy()
            self.create_password_popup()
        else:
            messagebox.showerror("Error", "IP Address yang dimasukkan tidak sesuai!") # Jika IP address tidak sesuai dengan IP address server

    def create_password_popup(self):
        """Pop-Up pengisian password chatroom"""
        self.password_popup = tk.Toplevel(self.root)
        self.password_popup.title("Enter Password")

        tk.Label(self.password_popup, text="Password:").grid(row=0, column=0)
        self.password_entry = tk.Entry(self.password_popup, show="*")
        self.password_entry.grid(row=0, column=1)

        submit_btn = tk.Button(self.password_popup, text="Submit", command=self.submit_password)
        submit_btn.grid(row=1, columnspan=2)

    def submit_password(self):
        """Validasi password"""
        self.password = self.password_entry.get()

        if self.password == var.password:
            self.password_popup.destroy()
            self.create_username_popup()
        else:
            messagebox.showerror("Error", "Password yang Anda masukkan salah!") # Jika password yang dimasukkan tidak sesuai

    def create_username_popup(self):
        """Pop-Up untuk pengisian username"""
        self.username_popup = tk.Toplevel(self.root)
        self.username_popup.title("Enter Username")

        tk.Label(self.username_popup, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.username_popup)
        self.username_entry.grid(row=0, column=1)

        submit_btn = tk.Button(self.username_popup, text="Submit", command=self.submit_username)
        submit_btn.grid(row=1, columnspan=2)

    def submit_username(self):
        """Validasi username"""
        self.name = self.username_entry.get()

        if self.name in existing_usernames:
            messagebox.showerror("Error", "Username already exists!") # Jika username sudah ada pada username .csv
        else:
            var.write_username(file_name, self.name)
            self.username_popup.destroy()
            self.create_chatroom_popup()

            threading.Thread(target=self.receive_messages, daemon=True).start()
            
    def create_chatroom_popup(self):
        """Tampilan Chatroom pada client"""
        self.chatroom_popup = tk.Toplevel(self.root)
        self.chatroom_popup.title(f"{self.name}'s Chatroom")

        self.chat_display = tk.Text(self.chatroom_popup, height=20, width=50)
        self.chat_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.chat_display.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(self.chatroom_popup, width=40)
        self.message_entry.grid(row=2, column=0, padx=5, pady=5)

        send_btn = tk.Button(self.chatroom_popup, text="Send", command=self.send_message, width=15)  # Wider Send button
        send_btn.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        exit_btn = tk.Button(self.chatroom_popup, text="Exit", command=self.exit_chat)
        exit_btn.grid(row=0, column=2, padx=(10, 5), pady=5, sticky="e")

        # Tanya apakah ingin restore history setelah chatroom dibuat
        restore_choice = messagebox.askquestion("Restore History", "Apakah anda ingin restore history chatroom?")
        
        if restore_choice == 'yes':
            messages = var.read_messages('messages.csv')
            if messages:
                self.chat_display.config(state=tk.NORMAL)
                for user, msg in messages:
                    self.chat_display.insert(tk.END, f"{user}: {msg}\n")
                self.chat_display.config(state=tk.DISABLED)

        client.sendto(f"SIGNUP_TAG:{self.name}".encode(), (self.IPaddress, self.portnum))

    def send_message(self):
        """Pengiriman pesan client"""
        message = self.message_entry.get()
        if message:
            client.sendto(f"{self.name}: {message}".encode(), (self.IPaddress, self.portnum))
            var.save_message('messages.csv', self.name, message)  # Simpan pesan ke CSV
            self.message_entry.delete(0, tk.END)

    def exit_chat(self):
        """Tombol untuk keluar dari chatroom"""
        client.sendto("!q".encode(), (self.IPaddress, self.portnum))
        var.delete_username(file_name, self.name)
        client.close()
        self.root.quit()

    
    def receive_messages(self):
        """Continuously receive messages from the server"""
        while True:
            try:
                message, _ = client.recvfrom(1024)
                decoded_message = message.decode()
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.insert(tk.END, decoded_message + "\n")
                self.chat_display.config(state=tk.DISABLED)
                
                # # Check for join and leave messages and display them
                # if "berhasil memasuki chatroom!" in decoded_message:
                #     # Highlight join message
                #     self.chat_display.config(state=tk.NORMAL)
                #     self.chat_display.insert(tk.END, f"{decoded_message}\n")
                #     self.chat_display.config(state=tk.DISABLED)
                # elif "telah keluar dari chatroom" in decoded_message:
                #     # Highlight leave message
                #     self.chat_display.config(state=tk.NORMAL)
                #     self.chat_display.insert(tk.END, f"{decoded_message}\n")
                #     self.chat_display.config(state=tk.DISABLED)
                # else:
                #     # Display normal messages
                #     self.chat_display.config(state=tk.NORMAL)
                #     self.chat_display.insert(tk.END, decoded_message + "\n")
                #     self.chat_display.config(state=tk.DISABLED)

                self.chat_display.yview(tk.END)  # Scroll to the end of the chat
            except:
                pass

# Fungsi menjalankan GUI client
def run_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    app = ChatroomApp(root)
    root.mainloop()
