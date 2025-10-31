import tkinter as tk
from tkinter import messagebox
import itertools

def faktorial(x):
    if x == 0 or x == 1:
        return 1
    hasil = 1
    for i in range(2, x + 1):
        hasil *= i
    return hasil

def kombinasi(n, r):
    if r > n:
        return 0
    return faktorial(n) // (faktorial(r) * faktorial(n - r))

def hitung_kombinasi():
    try:
        n = int(entry_n.get())
        r = int(entry_r.get())

        if r > n or n <= 0 or r <= 0:
            messagebox.showerror("Error", "Pastikan n ≥ r dan keduanya lebih dari 0.")
            return

        # Hitung kombinasi matematis
        hasil_jumlah = kombinasi(n, r)

        # Buat daftar huruf sesuai n (A, B, C, D, ...)
        huruf = [chr(65 + i) for i in range(n)]

        # Hitung kombinasi aktual
        semua_kombinasi = list(itertools.combinations(huruf, r))

        # Tampilkan hasil
        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(tk.END, f"Jumlah kombinasi C({n}, {r}) = {hasil_jumlah}\n\n")
        text_hasil.insert(tk.END, "=== Daftar Kombinasi Huruf ===\n")
        for i, combo in enumerate(semua_kombinasi, start=1):
            text_hasil.insert(tk.END, f"{i}. {' '.join(combo)}\n")

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

# GUI utama
root = tk.Tk()
root.title("Program Kombinasi Huruf")
root.geometry("550x500")
root.config(bg="#f0f4ff")

tk.Label(root, text="🔹 Program Kombinasi Huruf 🔹", font=("Segoe UI", 14, "bold"), bg="#f0f4ff").pack(pady=10)

frame_input = tk.Frame(root, bg="#f0f4ff")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Jumlah total objek (n):", bg="#f0f4ff", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5)
entry_n = tk.Entry(frame_input, width=10)
entry_n.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Jumlah objek yang dipilih (r):", bg="#f0f4ff", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5, pady=5)
entry_r = tk.Entry(frame_input, width=10)
entry_r.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Hitung Kombinasi", command=hitung_kombinasi,
           bg="#4a90e2", fg="white", font=("Segoe UI", 10, "bold"), width=25).pack(pady=10)

frame_hasil = tk.Frame(root, bg="#f0f4ff")
frame_hasil.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame_hasil)
scrollbar.pack(side="right", fill="y")

text_hasil = tk.Text(frame_hasil, wrap="word", yscrollcommand=scrollbar.set, font=("Consolas", 10))
text_hasil.pack(fill="both", expand=True)
scrollbar.config(command=text_hasil.yview)

root.mainloop()
