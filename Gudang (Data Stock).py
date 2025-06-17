import sqlite3
import getpass
import csv

# Koneksi database
conn = sqlite3.connect('gudang.db')
cur = conn.cursor()

# Buat tabel stok dan users jika belum ada
cur.execute('''
    CREATE TABLE IF NOT EXISTS stok (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        kategori TEXT,
        jumlah INTEGER NOT NULL
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit() # Menyimpan perubahan database

# Buat akun admin default
def seed_user():
    cur.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        conn.commit()

# Register user baru
def register():
    print("\n=== REGISTER PENGGUNA BARU ===")
    username = input("Buat Username: ")
    password = getpass.getpass("Buat Password: ")
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("✅ Akun berhasil dibuat.")
    except sqlite3.IntegrityError:
        print("❌ Username sudah digunakan. Coba lagi.")

# Login
def login():
    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    if user:
        print(f"✅ Login berhasil. Selamat datang, {username}!")
        return True
    else:
        print("❌ Username atau password salah.")
        return False

# Tambah barang
def tambah_barang():
    print("\n=== Tambah Barang ===")
    nama = input("Nama Barang: ")
    kategori = input("Kategori: ")
    try:
        jumlah = int(input("Jumlah: "))
        cur.execute("INSERT INTO stok (nama, kategori, jumlah) VALUES (?, ?, ?)", (nama, kategori, jumlah))
        conn.commit()
        print("✅ Barang berhasil ditambahkan.")
    except ValueError:
        print("⚠️ Jumlah harus berupa angka.")

# Tampilkan semua barang
def lihat_barang():
    print("\n=== Daftar Barang ===")
    cur.execute("SELECT * FROM stok")
    rows = cur.fetchall()
    if not rows:
        print("📭 Tidak ada data.")
    for row in rows:
        print(f"ID: {row[0]} | Nama: {row[1]} | Kategori: {row[2]} | Jumlah: {row[3]}")

# Cari barang
def cari_barang():
    print("\n=== Cari Barang ===")
    keyword = input("Masukkan nama atau sebagian nama barang: ")
    cur.execute("SELECT * FROM stok WHERE nama LIKE ?", ('%' + keyword + '%',))
    rows = cur.fetchall()
    if not rows:
        print("🔍 Tidak ditemukan.")
    for row in rows:
        print(f"ID: {row[0]} | Nama: {row[1]} | Kategori: {row[2]} | Jumlah: {row[3]}")

# Update barang
def update_barang():
    print("\n=== Update Barang ===")
    try:
        id_barang = int(input("ID Barang yang ingin diupdate: "))
        cur.execute("SELECT * FROM stok WHERE id=?", (id_barang,))
        if not cur.fetchone():
            print("❌ Barang tidak ditemukan.")
            return
        nama = input("Nama baru: ")
        kategori = input("Kategori baru: ")
        jumlah = int(input("Jumlah baru: "))
        cur.execute("UPDATE stok SET nama=?, kategori=?, jumlah=? WHERE id=?", (nama, kategori, jumlah, id_barang))
        conn.commit()
        print("🔁 Barang berhasil diupdate.")
    except ValueError:
        print("⚠️ Input tidak valid.")

# Hapus barang
def hapus_barang():
    print("\n=== Hapus Barang ===")
    try:
        id_barang = int(input("ID Barang yang ingin dihapus: "))
        cur.execute("SELECT * FROM stok WHERE id=?", (id_barang,))
        if not cur.fetchone():
            print("❌ Barang tidak ditemukan.")
            return
        cur.execute("DELETE FROM stok WHERE id=?", (id_barang,))
        conn.commit()
        print("🗑️ Barang berhasil dihapus.")
    except ValueError:
        print("⚠️ Input tidak valid.")

# Ekspor CSV
def ekspor_csv():
    print("\n=== Ekspor ke CSV ===")
    cur.execute("SELECT * FROM stok")
    rows = cur.fetchall()
    if not rows:
        print("📭 Tidak ada data untuk diekspor.")
        return
    with open('stok_gudang.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nama', 'Kategori', 'Jumlah'])
        writer.writerows(rows)
    print("📁 Data berhasil diekspor ke 'stok_gudang.csv'.")

# Menu utama
def main():
    seed_user()
    logged_in = False

    while True:
        print("\n=== MENU STOK GUDANG ===")
        print("1. Login")
        print("2. Register")
        print("3. Tambah Barang")
        print("4. Lihat Semua Barang")
        print("5. Cari Barang")
        print("6. Update Barang")
        print("7. Hapus Barang")
        print("8. Ekspor ke CSV")
        print("9. Keluar")

        pilihan = input("Pilih menu (1-9): ")

        if pilihan == "1":
            logged_in = login()
        elif pilihan == "2":
            register()
        elif pilihan in ["3", "4", "5", "6", "7", "8"] and not logged_in:
            print("🔒 Anda harus login dulu untuk mengakses fitur ini.")
        elif pilihan == "3":
            tambah_barang()
        elif pilihan == "4":
            lihat_barang()
        elif pilihan == "5":
            cari_barang()
        elif pilihan == "6":
            update_barang()
        elif pilihan == "7":
            hapus_barang()
        elif pilihan == "8":
            ekspor_csv()
        elif pilihan == "9":
            print("👋 Terima kasih. Program selesai.")
            break
        else:
            print("⚠️ Pilihan tidak valid. Coba lagi.")

    conn.close()

# Jalankan program
if __name__ == "__main__":
    main()
