import csv
password = "koplak"

# Fungsi untuk membaca username dalam username.csv
def read_usernames(file_name):
    usernames = []
    try:
        with open(file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            usernames = [row[0] for row in reader]
    except FileNotFoundError:
        # Jika file belum tersedia, akan membuat csv baru
        print(f"{file_name} tidak ditemukan, membuat file baru...")
    return usernames

# Fungsi untuk menuliskan username ke username.csv
def write_username(file_name, new_username):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_username])  

# Fungsi untuk menghapus username yang akan digunakan saat client keluar dari chatroom
def delete_username(file_name, username):
    usernames = read_usernames(file_name)
    usernames = [user for user in usernames if user != username]  
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for user in usernames:
            writer.writerow([user]) 

# Fungsi untuk menyimpan pesan ke dalam messages.csv, yang akan digunakan pada implementasi restore history chatroom
def save_message(file_name, username, message):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, message])

# Fungsi untuk membaca pesan dalam messages.csv
def read_messages(file_name):
    messages = []
    try:
        with open(file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            messages = [row for row in reader]
    except FileNotFoundError:
        # Jika belum ada file messages.csv, akan membuat file csv baru
        print(f"{file_name} tidak ditemukan, membuat file baru...")
    return messages 