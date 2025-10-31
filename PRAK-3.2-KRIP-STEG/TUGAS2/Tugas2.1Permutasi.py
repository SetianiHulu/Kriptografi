import itertools
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# === FUNGSI PERMUTASI ===
def permutasi_menyeluruh(data):
    return list(itertools.permutations(data))

def permutasi_sebagian(data, k):
    return list(itertools.permutations(data, k))

def permutasi_keliling(data):
    if len(data) <= 1:
        return [data]
    pertama = data[0]
    hasil = []
    for perm in itertools.permutations(data[1:]):
        hasil.append([pertama] + list(perm))
    return hasil

def permutasi_berkelompok(grup):
    hasil = [[]]
    for kelompok in grup:
        hasil_baru = []
        for hsl in hasil:
            for perm in itertools.permutations(kelompok):
                hasil_baru.append(hsl + list(perm))
        hasil = hasil_baru
    return hasil

# === FUNGSI UTAMA TAMPILAN DAN EKSEKUSI ===
def tampilkan_hasil(judul, hasil):
    output_box.config(state='normal')
    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, f"=== {judul} ===\n", "judul")
    output_box.insert(tk.END, f"Jumlah hasil: {len(hasil)}\n\n", "info")
    for h in hasil:
        output_box.insert(tk.END, " ".join(str(x) for x in h) + "\n")
    output_box.config(state='disabled')

def konfirmasi_lanjut():
    jawab = messagebox.askyesno("Konfirmasi", "Apakah Anda ingin melanjutkan program?")
    if not jawab:
        root.destroy()

def jalankan_permutasi_menyeluruh():
    data = simpledialog.askstring("Input Data", "Masukkan elemen (pisahkan dengan spasi):")
    if not data: return
    data = data.split()
    hasil = permutasi_menyeluruh(data)
    tampilkan_hasil("Permutasi Menyeluruh", hasil)
    konfirmasi_lanjut()

def jalankan_permutasi_sebagian():
    data = simpledialog.askstring("Input Data", "Masukkan elemen (pisahkan dengan spasi):")
    if not data: return
    data = data.split()
    k = simpledialog.askinteger("Input K", f"Masukkan jumlah elemen yang diambil (1 - {len(data)}):")
    if not k: return
    hasil = permutasi_sebagian(data, k)
    tampilkan_hasil("Permutasi Sebagian", hasil)
    konfirmasi_lanjut()

def jalankan_permutasi_keliling():
    data = simpledialog.askstring("Input Data", "Masukkan elemen (pisahkan dengan spasi):")
    if not data: return
    data = data.split()
    hasil = permutasi_keliling(data)
    tampilkan_hasil("Permutasi Keliling", hasil)
    konfirmasi_lanjut()

def jalankan_permutasi_berkelompok():
    jml_grup = simpledialog.askinteger("Input Jumlah Grup", "Masukkan jumlah grup:")
    if not jml_grup: return
    grup = []
    for i in range(jml_grup):
        anggota = simpledialog.askstring("Input Grup", f"Masukkan anggota grup {i+1} (pisahkan dengan spasi):")
        if not anggota: return
        grup.append(anggota.split())
    hasil = permutasi_berkelompok(grup)
    tampilkan_hasil("Permutasi Berkelompok", hasil)
    konfirmasi_lanjut()

# === GUI UTAMA ===
root = tk.Tk()
root.title("💠 Program Permutasi GUI - Praktikum 3")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="#f4f6f7")

# === HEADER ===
header_frame = tk.Frame(root, bg="#3498db")
header_frame.pack(fill='x')

tk.Label(header_frame, text="PROGRAM PERMUTASI", font=("Helvetica", 16, "bold"), bg="#3498db", fg="white").pack(pady=10)
tk.Label(header_frame, text="(Menyeluruh, Sebagian, Keliling, Berkelompok)", font=("Helvetica", 11), bg="#3498db", fg="white").pack(pady=(0,10))

# === FRAME TOMBOL ===
menu_frame = tk.Frame(root, bg="#f4f6f7")
menu_frame.pack(pady=20)

button_style = {"font": ("Arial", 11, "bold"), "width": 25, "height": 2, "bd": 0, "relief": "flat"}

def buat_tombol(teks, warna, perintah, baris, kolom):
    tk.Button(menu_frame, text=teks, bg=warna, fg="white",
              activebackground="#2c3e50", activeforeground="white",
              command=perintah, **button_style).grid(row=baris, column=kolom, padx=10, pady=8)

buat_tombol("🔹 Permutasi Menyeluruh", "#27ae60", jalankan_permutasi_menyeluruh, 0, 0)
buat_tombol("🔸 Permutasi Sebagian", "#2980b9", jalankan_permutasi_sebagian, 0, 1)
buat_tombol("🔹 Permutasi Keliling", "#e67e22", jalankan_permutasi_keliling, 1, 0)
buat_tombol("🔸 Permutasi Berkelompok", "#8e44ad", jalankan_permutasi_berkelompok, 1, 1)

# === OUTPUT BOX ===
output_box = scrolledtext.ScrolledText(root, width=80, height=15, font=("Consolas", 10), wrap='word', bg="#ffffff", fg="#2c3e50")
output_box.tag_configure("judul", font=("Arial", 11, "bold"), foreground="#2980b9")
output_box.tag_configure("info", font=("Arial", 10, "italic"), foreground="#16a085")
output_box.pack(padx=15, pady=15)
output_box.config(state='disabled')

# === FOOTER DAN EXIT ===
footer_frame = tk.Frame(root, bg="#f4f6f7")
footer_frame.pack(pady=5)

tk.Button(footer_frame, text="❌ Keluar", command=root.destroy, bg="#c0392b", fg="white",
          font=("Arial", 10, "bold"), width=20, height=2, relief="flat").pack(pady=5)

tk.Label(root, text="© 2025 | Praktikum 3 - Setiany Hulu", bg="#f4f6f7", fg="#7f8c8d", font=("Arial", 9)).pack(side="bottom", pady=5)

root.mainloop()
