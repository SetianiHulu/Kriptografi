import tkinter as tk
from tkinter import messagebox, scrolledtext

# === Fungsi Transposisi Cipher ===
def transposisi_cipher(plaintext, kolom):
    panjang_bagian = len(plaintext) // kolom
    if len(plaintext) % kolom != 0:
        panjang_bagian += 1

    # Bagi teks menjadi blok/blok bagian
    parts = [plaintext[i:i + panjang_bagian] for i in range(0, len(plaintext), panjang_bagian)]
    
    output_box.insert(tk.END, "=== Bagian Plaintext ===\n")
    for i, part in enumerate(parts):
        output_box.insert(tk.END, f"Bagian {i+1}: '{part}'\n")

    ciphertext = ""
    output_box.insert(tk.END, "\n=== Proses Transposisi ===\n")

    for col in range(kolom):
        for part in parts:
            if col < len(part):
                ciphertext += part[col]
                output_box.insert(tk.END, f"Menambahkan '{part[col]}' dari Bagian {parts.index(part)+1}\n")

    return ciphertext


# === Fungsi tombol proses ===
def jalankan_transposisi():
    plaintext = entry_plaintext.get()
    try:
        kolom = int(entry_kolom.get())
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka valid untuk jumlah kolom!")
        return

    if not plaintext:
        messagebox.showwarning("Peringatan", "Masukkan plaintext terlebih dahulu!")
        return

    output_box.delete("1.0", tk.END)
    ciphertext = transposisi_cipher(plaintext, kolom)

    output_box.insert(tk.END, "\n=== HASIL AKHIR ===\n")
    output_box.insert(tk.END, f"Plaintext : {plaintext}\n")
    output_box.insert(tk.END, f"Ciphertext: {ciphertext}\n")


# === GUI Tkinter ===
root = tk.Tk()
root.title("Transposisi Cipher - Kriptografi Klasik")
root.geometry("700x600")
root.resizable(False, False)

tk.Label(root, text="🔐 Transposisi Cipher", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(root, text="Program untuk mengubah urutan huruf teks (Transposisi)", font=("Arial", 11)).pack()

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Masukkan Plaintext:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_plaintext = tk.Entry(frame_input, width=40, font=("Arial", 12))
entry_plaintext.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Jumlah Kolom:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_kolom = tk.Entry(frame_input, width=10, font=("Arial", 12))
entry_kolom.insert(0, "4")
entry_kolom.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Button(root, text="Proses Transposisi", command=jalankan_transposisi,
          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20).pack(pady=10)

output_box = scrolledtext.ScrolledText(root, width=80, height=20, font=("Courier New", 11))
output_box.pack(padx=10, pady=10)

tk.Button(root, text="Keluar", command=root.destroy, bg="red", fg="white", width=15).pack(pady=5)

root.mainloop()
