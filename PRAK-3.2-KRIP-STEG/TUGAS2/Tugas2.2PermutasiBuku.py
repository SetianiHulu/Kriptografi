import tkinter as tk
from tkinter import messagebox, ttk
import itertools

def hitung_pengaturan():
    try:
        n = int(entry_n.get())
        r = int(entry_r.get())

        if n <= 0 or r <= 0:
            messagebox.showerror("Error", "Jumlah buku dan rak harus lebih dari 0.")
            return

        # Membuat daftar nama buku dan rak
        buku = [f"B{i+1}" for i in range(n)]
        rak = [f"R{j+1}" for j in range(r)]

        # Menghasilkan semua kombinasi
        hasil = list(itertools.product(rak, repeat=n))

        # Tampilkan di area teks
        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(tk.END, f"Jumlah Buku: {n}, Jumlah Rak: {r}\n")
        text_hasil.insert(tk.END, f"Total Kemungkinan: {len(hasil)}\n\n")

        for i, kombinasi in enumerate(hasil, start=1):
            pasangan = [f"{buku[j]}->{kombinasi[j]}" for j in range(n)]
            text_hasil.insert(tk.END, f"{i}. {', '.join(pasangan)}\n")

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

# Membuat jendela utama
root = tk.Tk()
root.title("Program Pengaturan Buku di Rak")
root.geometry("600x500")
root.config(bg="#e8f0fe")

# Judul
label_judul = tk.Label(root, text="🔹 Program Pengaturan Buku di Rak 🔹",
                       font=("Segoe UI", 14, "bold"), bg="#e8f0fe")
label_judul.pack(pady=10)

# Frame input
frame_input = tk.Frame(root, bg="#e8f0fe")
frame_input.pack(pady=5)

tk.Label(frame_input, text="Jumlah Buku (n):", font=("Segoe UI", 10), bg="#e8f0fe").grid(row=0, column=0, padx=5, pady=5)
entry_n = tk.Entry(frame_input, width=10)
entry_n.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Jumlah Rak (r):", font=("Segoe UI", 10), bg="#e8f0fe").grid(row=1, column=0, padx=5, pady=5)
entry_r = tk.Entry(frame_input, width=10)
entry_r.grid(row=1, column=1, padx=5, pady=5)

# Tombol
btn_hitung = tk.Button(root, text="Hitung Semua Pengaturan", command=hitung_pengaturan,
                       bg="#4a90e2", fg="white", font=("Segoe UI", 10, "bold"), width=30)
btn_hitung.pack(pady=10)

# Area hasil
frame_hasil = tk.Frame(root, bg="#e8f0fe")
frame_hasil.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame_hasil)
scrollbar.pack(side="right", fill="y")

text_hasil = tk.Text(frame_hasil, wrap="word", yscrollcommand=scrollbar.set, font=("Consolas", 10))
text_hasil.pack(fill="both", expand=True)
scrollbar.config(command=text_hasil.yview)

# Jalankan aplikasi
root.mainloop()
