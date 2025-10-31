import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image

# === FUNGSI ENKRIPSI / DEKRIPSI ===
def buat_peta_permutasi(permutasi):
    alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    permutasi = permutasi.upper()
    if len(permutasi) != 26 or set(permutasi) != set(alfabet):
        messagebox.showerror("Kesalahan", "Permutasi harus terdiri dari 26 huruf unik (A-Z).")
        return None, None
    enkripsi_map = str.maketrans(alfabet, permutasi)
    dekripsi_map = str.maketrans(permutasi, alfabet)
    return enkripsi_map, dekripsi_map

def enkripsi(teks, enkripsi_map):
    return teks.upper().translate(enkripsi_map)

def dekripsi(teks, dekripsi_map):
    return teks.upper().translate(dekripsi_map)

# === FUNGSI STEGANOGRAFI ===
def sisipkan_pesan(gambar_path, pesan, output_path):
    img = Image.open(gambar_path).convert('RGB')
    biner_pesan = ''.join(format(ord(c), '08b') for c in pesan) + '1111111111111110'  # Penanda akhir
    data = list(img.getdata())
    if len(biner_pesan) > len(data) * 3:
        messagebox.showerror("Error", "Pesan terlalu panjang untuk gambar ini.")
        return
    idx = 0
    new_data = []
    for pixel in data:
        r, g, b = pixel
        if idx < len(biner_pesan):
            r = (r & ~1) | int(biner_pesan[idx]); idx += 1
        if idx < len(biner_pesan):
            g = (g & ~1) | int(biner_pesan[idx]); idx += 1
        if idx < len(biner_pesan):
            b = (b & ~1) | int(biner_pesan[idx]); idx += 1
        new_data.append((r, g, b))
    img.putdata(new_data)
    img.save(output_path)
    messagebox.showinfo("Berhasil", f"Pesan berhasil disisipkan ke gambar:\n{output_path}")

def ekstrak_pesan(gambar_path):
    img = Image.open(gambar_path)
    data = list(img.getdata())
    biner_pesan = ''
    for pixel in data:
        for warna in pixel[:3]:
            biner_pesan += str(warna & 1)
    byte_list = [biner_pesan[i:i+8] for i in range(0, len(biner_pesan), 8)]
    pesan = ''
    for byte in byte_list:
        if byte == '11111110':  # penanda akhir
            break
        pesan += chr(int(byte, 2))
    messagebox.showinfo("Pesan Tersembunyi", f"Pesan yang diekstrak:\n\n{pesan}")

# === GUI UTAMA ===
root = tk.Tk()
root.title("🔐 Program Kriptografi & Steganografi")
root.geometry("650x550")
root.configure(bg="#f7f7f7")
root.resizable(False, False)

# === JUDUL ===
judul = tk.Label(root, 
    text="PROGRAM KRIPTOGRAFI & STEGANOGRAFI",
    font=("Helvetica", 16, "bold"),
    bg="#f7f7f7",
    fg="#2a2a2a"
)
judul.pack(pady=10)

subjudul = tk.Label(root, 
    text="Kembangkan agar semua jenis permutasi dapat diinput dari keyboard",
    font=("Arial", 10),
    bg="#f7f7f7",
    fg="#555"
)
subjudul.pack(pady=5)

# Variabel global
enkripsi_map = None
dekripsi_map = None

# === BAGIAN FUNGSI ===
def atur_permutasi():
    global enkripsi_map, dekripsi_map
    perm = simpledialog.askstring(
        "Input Permutasi",
        "Masukkan 26 huruf A-Z secara acak (tanpa spasi):"
    )
    if not perm:
        return
    hasil = buat_peta_permutasi(perm)
    if hasil[0]:
        enkripsi_map, dekripsi_map = hasil
        messagebox.showinfo("Sukses", "Permutasi berhasil disimpan!\nSekarang Anda dapat melakukan enkripsi atau dekripsi.")

def menu_enkripsi():
    if not enkripsi_map:
        messagebox.showwarning("Peringatan", "Masukkan permutasi huruf terlebih dahulu!")
        return
    teks = simpledialog.askstring("Enkripsi", "Masukkan teks yang akan dienkripsi:")
    if teks:
        hasil = enkripsi(teks, enkripsi_map)
        messagebox.showinfo("Hasil Enkripsi", f"Ciphertext:\n\n{hasil}")

def menu_dekripsi():
    if not dekripsi_map:
        messagebox.showwarning("Peringatan", "Masukkan permutasi huruf terlebih dahulu!")
        return
    teks = simpledialog.askstring("Dekripsi", "Masukkan ciphertext yang akan didekripsi:")
    if teks:
        hasil = dekripsi(teks, dekripsi_map)
        messagebox.showinfo("Hasil Dekripsi", f"Plaintext:\n\n{hasil}")

def menu_sisipkan_pesan():
    gambar_path = filedialog.askopenfilename(title="Pilih Gambar", filetypes=[("Image files", "*.png;*.jpg;*.bmp")])
    if not gambar_path:
        return
    pesan = simpledialog.askstring("Pesan", "Masukkan pesan yang akan disembunyikan:")
    if not pesan:
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".png", title="Simpan Gambar Baru", filetypes=[("PNG Image", "*.png")])
    if output_path:
        sisipkan_pesan(gambar_path, pesan, output_path)

def menu_ekstrak_pesan():
    gambar_path = filedialog.askopenfilename(title="Pilih Gambar", filetypes=[("Image files", "*.png;*.jpg;*.bmp")])
    if gambar_path:
        ekstrak_pesan(gambar_path)

# === TATA LETAK TOMBOL ===
frame = tk.Frame(root, bg="#f7f7f7")
frame.pack(pady=20)

tombol_style = {"width": 28, "height": 2, "font": ("Arial", 10, "bold")}

tk.Button(frame, text="1️⃣ Atur Permutasi Huruf", command=atur_permutasi, bg="#4CAF50", fg="white", **tombol_style).grid(row=0, column=0, padx=10, pady=8)
tk.Button(frame, text="2️⃣ Enkripsi Teks", command=menu_enkripsi, bg="#2196F3", fg="white", **tombol_style).grid(row=0, column=1, padx=10, pady=8)
tk.Button(frame, text="3️⃣ Dekripsi Teks", command=menu_dekripsi, bg="#FF9800", fg="white", **tombol_style).grid(row=1, column=0, padx=10, pady=8)
tk.Button(frame, text="4️⃣ Sisipkan Pesan ke Gambar", command=menu_sisipkan_pesan, bg="#9C27B0", fg="white", **tombol_style).grid(row=1, column=1, padx=10, pady=8)
tk.Button(frame, text="5️⃣ Ekstrak Pesan dari Gambar", command=menu_ekstrak_pesan, bg="#795548", fg="white", **tombol_style).grid(row=2, column=0, columnspan=2, pady=8)

# Tombol keluar
tk.Button(root, text="Keluar", command=root.destroy, bg="red", fg="white", font=("Arial", 10, "bold"), width=20, height=2).pack(pady=10)

# Footer
footer = tk.Label(root, text="© 2025 | Praktikum Kriptografi & Steganografi - by Setiany Hulu", bg="#f7f7f7", fg="#888", font=("Arial", 9))
footer.pack(side="bottom", pady=5)

root.mainloop()
