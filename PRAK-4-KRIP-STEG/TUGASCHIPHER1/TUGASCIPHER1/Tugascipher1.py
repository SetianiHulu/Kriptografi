import tkinter as tk
from tkinter import messagebox, scrolledtext

# === Fungsi Substitusi Cipher ===
def buat_aturan_substitusi():
    aturan = {}
    huruf = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for h in huruf:
        pengganti = entries[h].get().upper()
        if pengganti == "":
            pengganti = h
        aturan[h] = pengganti
    return aturan

def substitusi_cipher(plaintext, aturan):
    ciphertext = ""
    for char in plaintext.upper():
        if char in aturan:
            ciphertext += aturan[char]
        else:
            ciphertext += char
    return ciphertext

def proses_enkripsi():
    plaintext = entry_plaintext.get().upper()
    if not plaintext:
        messagebox.showwarning("Peringatan", "Masukkan plaintext terlebih dahulu!")
        return

    aturan = buat_aturan_substitusi()
    ciphertext = substitusi_cipher(plaintext, aturan)

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Plaintext : {plaintext}\n")
    output_box.insert(tk.END, f"Ciphertext: {ciphertext}\n")

# === GUI Utama ===
root = tk.Tk()
root.title("Substitusi Cipher - Kriptografi Klasik")
root.geometry("700x600")
root.resizable(False, False)

# Judul
tk.Label(root, text="🔐 Substitusi Cipher", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(root, text="Masukkan plaintext dan atur pengganti huruf A-Z", font=("Arial", 11)).pack()

# Input plaintext
frame_input = tk.Frame(root)
frame_input.pack(pady=10)
tk.Label(frame_input, text="Plaintext: ", font=("Arial", 12)).grid(row=0, column=0, padx=5)
entry_plaintext = tk.Entry(frame_input, width=40, font=("Arial", 12))
entry_plaintext.grid(row=0, column=1, padx=5)

# Aturan substitusi
frame_aturan = tk.LabelFrame(root, text="Aturan Substitusi Huruf (A → ?)", font=("Arial", 11, "bold"))
frame_aturan.pack(padx=10, pady=10)

entries = {}
huruf = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i, h in enumerate(huruf):
    tk.Label(frame_aturan, text=f"{h} →", font=("Arial", 10)).grid(row=i//6, column=(i%6)*2, padx=3, pady=3)
    e = tk.Entry(frame_aturan, width=3, font=("Arial", 10), justify="center")
    e.grid(row=i//6, column=(i%6)*2+1, padx=3, pady=3)
    entries[h] = e

# Tombol proses
tk.Button(root, text="Enkripsi Sekarang", command=proses_enkripsi,
          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20).pack(pady=10)

# Output box
output_box = scrolledtext.ScrolledText(root, width=80, height=10, font=("Courier New", 11))
output_box.pack(padx=10, pady=10)

# Tombol keluar
tk.Button(root, text="Keluar", command=root.destroy, bg="red", fg="white", width=15).pack(pady=5)

root.mainloop()
