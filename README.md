# Maze Game
# Deskripsi
Proyek ini merupakan sebuah game RPG sederhana berbasis 2D yang dibuat menggunakan bahasa pemrograman Python dengan library Pygame. Game ini mengusung konsep petualangan di dalam dungeon atau labirin, di mana pemain harus menjelajahi area, menghindari jebakan, mencari kunci, membuka pintu, dan mengambil peti harta untuk menyelesaikan misi.
# Anggota Kelompok
1. Nayaka Raya Archie Setianto (25051204001) - Pembuat Class + cerita
2. Syifa'ul Iqbal Saputra (25051204007) – Pembuat map + FOV
3. Pobi Putra Anugrah (25051204074) – Pembuat map + Assets
4. Faid Haidar (25051204152) – Pembuat Class + cerita
# Fitur utama
1. Sistem Pergerakan Player
   Player dapat bergerak ke arah kiri, kanan, atas, dan bawah menggunakan arrow key pada keyboard.
2. Camera Follow
   Kamera akan mengikuti posisi player dari atas.
3. Sprite Animation
   Karakter player memiliki animasi idle dan berjalan menggunakan sprite sheet agar karakter terlihat hidup.
4. Collision
   Player tidak dapat menembus tembok dan pintu yang masih terkunci.
5. Sistem Dungeon Tileset
   Map menggunakan assets yang dipasang sedemikian rupa sehingga terlihat seperti labirin bawah tanah.
6. Interaction
   Player dapat berinteraksi dengan NPC dengan menekan tombol spasi untuk mendapatkan misi, dialog, atau beberapa interaksi lainnya.
7. Misi
   Player diharuskan mengambil peti harta sebagai tujuan utama permainan.
8. Sistem pintu terkunci
   Player harus mencari kunci terlebih dahulu untuk membuka pintu.
9. Jebakan
   Terdapat jebakan pada beberapa bagian pada map yang menyebabkan player mati jika terkena.
10. Respawn
    Setelah terkena jebakan, player dapat hidup kembali dan kembali ke titik awal permainan.
# Cara menjalankan game
1. Download/install python versi dibawah 3.14 atau versi yang bisa menjalankan Pygame.
2. Install pygame dengan cara buka terminal dan jalankan command "pip install pygame".
3. Download folder "final project" pada github ini dan pastikan semua isinya masuk ke folder yang sama.
4. Buka file "MazeGame.py" di terminal atau di Visual Studio Code
5. Control : Arrow key/tombol panah untuk menggerakkan karakter, Space/spasi untuk interaksi, Esc untuk keluar game.
   
# Panduan Bermain
1. Pemain harus menemukan dan interaksi npc/villager terlebih dahulu
2. didekat villager akan ada sebuah kunci, ambil untuk membuka pintu
3. cari ruangan yang memiliki pintu (hati-hati ada 1 pintu yang mengarah jebakan
4. cari sebuah chest dan kembali ke villager/npc untuk menyelesaikan gamenya

# Latar Belakang game
Di suatu masa yang teramat lampau dunia dipenuhi oleh reruntuhan tak terhitung. Mercenary yang amat banyak telah berpetualang menyusuri reruntuhan, tak terhitung juga mercenary yang telah tiada didalam reruntuhan, Ini semua untuk mendapatkan peti harta karun yang sudah dicari begitu lama oleh sang Raja, Raja tersebut memiliki seorang Putri yang sedang sakit. Konon di dalam reruntuhan yang sangat rumit bahkan banyak mercenary gagal menyelesaikan ekspedisi di reruntuhan tersebut terdapat sebuah peti yang berisi ramuan yang dapat menyembuhkan penyakit sang Putri dari penyakitnya. Penyakit tersebut telah membuat sang Putri begitu tersiksa, sehingga membuat sang Raja akhirnya membuat sebuah Titah ke semua guild mercenary untuk menyebarkan sebuah tugas dengan hadiah fantastis yang berupa harta yang melimpah dan dapat menikahi sang putri.

Ribuan mercenary akhirnya berlomba untuk mencari tahu keberadaan reruntuhan yang terdapat peti tersebut. Beberapa tahun telah berlalu dan akhirnya seorang mercenary menemukan sebuah reruntuhan yang dirumorkan tersebut. Walau sang mercenary telah menemukan reruntuhan tersebut ia harus bisa melewati berbagai rintangan yang ada didalam untuk mendapatkan peti tersebut, Namun yang tidak di sangka reruntuhan tersebut ternyata memiliki labirin yang gelap gulita serta rumit yang dapat membingungkan mercenary yang mencoba menyelesaikan ekspedisi didalam reruntuhan tersebut.

Dengan pencahayaan yang minim, banyaknya jebakan, serta harus mencari kunci yang digunakan untuk membuka berbagai ruangan Akankah Sang Mercenary berhasil mendapatkan peti tersebut?
