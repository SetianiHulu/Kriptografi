import tkinter as tk
from tkinter import messagebox, scrolledtext

# === FUNGSI PROSES ===

def proses_cipher():
    teks = entry_plain.get().upper().replace(" ", "")
    if not teks:
        messagebox.showwarning("Peringatan", "Masukkan teks terlebih dahulu!")
        return

    aturan_input = entry_aturan.get("1.0", tk.END).strip().upper()
    aturan_baru = {}

    try:
        for baris in aturan_input.splitlines():
            if "=" in baris:
                kiri, kanan = baris.split("=")
                kiri = kiri.strip()
                kanan = kanan.strip()
                if len(kiri) == 1 and len(kanan) == 1 and kiri.isalpha() and kanan.isalpha():
                    aturan_baru[kiri] = kanan
                else:
                    raise ValueError
        if not aturan_baru:
            raise ValueError
    except:
        messagebox.showerror("Kesalahan", "Format aturan salah!\nGunakan format: A = Q, B = W, dst.")
        return

    # Substitusi
    hasil_subs = ""
    for c in teks:
        if c in aturan_baru:
            hasil_subs += aturan_baru[c]
        else:
            hasil_subs += c

    # Transposisi (4 kolom)
    blok = 4
    baris = [hasil_subs[i:i + blok] for i in range(0, len(hasil_subs), blok)]

    # Menampilkan tabel transposisi
    tabel = "=== Transposisi (4 Kolom) ===\n"
    tabel += "-------------------------\n"
    for b in baris:
        tabel += " | ".join(f"{ch:^3}" for ch in b) + "\n"
    tabel += "-------------------------\n"

    hasil_trans = ""
    for i in range(blok):
        for b in baris:
            if i < len(b):
                hasil_trans += b[i]

    # Tampilkan hasil di GUI
    hasil_output.config(state="normal")
    hasil_output.delete("1.0", tk.END)
    hasil_output.insert(tk.END, f"Hasil Substitusi:\n{hasil_subs}\n\n{tabel}\nCipher Akhir:\n{hasil_trans}")
    hasil_output.config(state="disabled")


# === GUI ===

root = tk.Tk()
root.title("Program Substitusi + Transposisi Cipher")
root.geometry("600x600")
root.config(bg="#eef2f3")

# Judul
judul = tk.Label(root, text="🔐 Substitusi + Transposisi Cipher", font=("Arial", 16, "bold"), bg="#eef2f3", fg="#333")
judul.pack(pady=10)

# Input teks
frame_input = tk.Frame(root, bg="#eef2f3")
frame_input.pack(pady=5)
tk.Label(frame_input, text="Masukkan Teks:", font=("Arial", 12), bg="#eef2f3").grid(row=0, column=0, padx=10)
entry_plain = tk.Entry(frame_input, width=40, font=("Arial", 12))
entry_plain.grid(row=0, column=1)

# Aturan substitusi
tk.Label(root, text="Aturan Substitusi (contoh: A = Q)", font=("Arial", 12, "bold"), bg="#eef2f3").pack(pady=5)
entry_aturan = scrolledtext.ScrolledText(root, width=50, height=10, font=("Consolas", 12))
entry_aturan.pack()

# Tombol proses
btn_proses = tk.Button(root, text="Proses Cipher", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20, command=proses_cipher)
btn_proses.pack(pady=10)

# Hasil output
tk.Label(root, text="Hasil:", font=("Arial", 12, "bold"), bg="#eef2f3").pack()
hasil_output = scrolledtext.ScrolledText(root, width=60, height=12, font=("Consolas", 12))
hasil_output.pack(pady=5)
hasil_output.config(state="disabled")

# Tombol keluar
tk.Button(root, text="Keluar", font=("Arial", 11, "bold"), bg="#f44336", fg="white", width=10, command=root.destroy).pack(pady=10)

root.mainloop()