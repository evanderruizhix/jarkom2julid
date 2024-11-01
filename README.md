# Tugas Besar Jaringan Komputer
Anggota Kelompok:
1. Favian Rafi Laftiyanto (18223036)
2. Ahmad Evander Ruizhi Xavier (18223064)

# Penjelasan Singkat
Program ini merupakan program chatroom berbasis UDP (User Data Protocol) yang memungkinkan banyak client untuk bergabung ke dalam sebuah chatroom yang dikelola oleh server. Pada chatroom, client dapat mengirim dan menerima pesan secara real-time. 

# Cara menggunakan Program
1. Run server.py terlebih dahulu.
2. Run client.py sebanyak yang diinginkan pada device yang sudah terhubung di sebuah network di Hamachi.
3. Masukkan IP Address, Portnum, Password, dan Username yang diinginkan.
4. Client dapat memilih restore history atau tidak.
5. Client dapat berinteraksi dengan client lain layaknya sebuah chatroom.

# Alur Server
1. Server dinyalakan oleh suatu device.
2. Setelah menyala, server akan mendengarkan koneksi dari client. Ketika client mengirimkan pesan, server akan menampilkannya pada GUI server, kemudian mendistribusikannya ke semua client yang terhubung.
3. Ketika ada client yang bergabung atau keluar dari chatroom, server akan menampilkan pesan log bahwa client tersebut telah berhasil memasuki chatroom atau client tersebut keluar dari chatroom.

# Alur Client
1. Setelah server dinyalakan pada suatu device, client dapat menjalankan program baik pada device yang sama atau device yang berbeda (Pastikan server dan client menggunakan Hamachi sehingga dapat terhubung dan pesan bisa sampai).
2. Ketika program client dijalankan, client akan diminta untuk mengisi IP Address dan Port Number tujuan pada pop-up yang muncul, lalu mengisi Password chatroom pada pop-up berikutnya. IP address dan Password chatroom yang dimasukkan harus sesuai. (NOTE: Tidak dilakukan pengecekan Port Number, namun apabila Portnum yang dimasukkan tidak sesuai, pesan tidak dapat sampai di server)
3. Setelah mengisi password, akan muncul pop-up berikutnya untuk mengisi username. Apabila username tersedia (maksudnya belum ada client lain yang menggunakan), maka username yang dimasukkan oleh client akan dimasukkan ke dalam file username.csv sehingga tidak ada user lain yang dapat menggunakan username yang sama.
4. Setelah itu, akan tampil tampilan message chatroom dan juga pop-up pertanyaan “Apakah ingin restore history?”, jika client menekan “yes”, maka program akan membaca pesan lampau yang tersimpan pada messages.csv
5. Melalui tampilan message chatroom, client dapat mengetik pesan yang ingin dikirimkan dan juga membaca pesan dari client lain yang terhubung layaknya chatroom pada umumnya.
