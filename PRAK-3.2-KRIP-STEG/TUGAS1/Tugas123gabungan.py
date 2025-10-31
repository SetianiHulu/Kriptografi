import tkinter as tk
from tkinter import ttk, messagebox

# === Fungsi Konversi ===
def konversi_bilangan():
    try:
        nilai = entry_input.get().strip()
        jenis = combo_pilihan.get()

        if not nilai:
            messagebox.showwarning("Peringatan", "Masukkan nilai bilangan terlebih dahulu!")
            return

        if jenis == "Desimal":
            desimal = int(nilai)
        elif jenis == "Biner":
            desimal = int(nilai, 2)
        elif jenis == "Oktal":
            desimal = int(nilai, 8)
        elif jenis == "Heksadesimal":
            desimal = int(nilai, 16)
        else:
            messagebox.showerror("Error", "Jenis bilangan tidak valid!")
            return

        # Hasil konversi
        hasil_biner = bin(desimal)[2:]
        hasil_oktal = oct(desimal)[2:]
        hasil_heksa = hex(desimal)[2:].upper()

        # Tampilkan hasil di label
        label_hasil.config(
            text=(
                f"=== HASIL KONVERSI ===\n"
                f"Desimal      : {desimal}\n"
                f"Biner        : {hasil_biner}\n"
                f"Oktal        : {hasil_oktal}\n"
                f"Heksadesimal : {hasil_heksa}"
            )
        )

    except ValueError:
        messagebox.showerror("Kesalahan Input", "Masukkan bilangan yang valid sesuai jenisnya!")

# === Fungsi Keluar ===
def keluar():
    if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
        root.destroy()

# === Tampilan Utama ===
root = tk.Tk()
root.title("Aplikasi Konversi Bilangan")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#F7F7F7")

# Judul
judul = tk.Label(
    root,
    text="💡 Konversi Bilangan (Desimal, Biner, Oktal, Heksadesimal)",
    font=("Arial", 12, "bold"),
    bg="#F7F7F7",
    fg="#333"
)
judul.pack(pady=15)

# Frame input
frame_input = tk.Frame(root, bg="#F7F7F7")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Masukkan Nilai:", font=("Arial", 11), bg="#F7F7F7").grid(row=0, column=0, padx=5, pady=5)
entry_input = tk.Entry(frame_input, width=25, font=("Arial", 11))
entry_input.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Jenis Bilangan:", font=("Arial", 11), bg="#F7F7F7").grid(row=1, column=0, padx=5, pady=5)
combo_pilihan = ttk.Combobox(frame_input, values=["Desimal", "Biner", "Oktal", "Heksadesimal"], width=22, font=("Arial", 11))
combo_pilihan.grid(row=1, column=1, padx=5, pady=5)
combo_pilihan.current(0)

# Tombol konversi
frame_tombol = tk.Frame(root, bg="#F7F7F7")
frame_tombol.pack(pady=10)

btn_konversi = tk.Button(frame_tombol, text="Konversi", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=15, command=konversi_bilangan)
btn_konversi.grid(row=0, column=0, padx=10)

btn_keluar = tk.Button(frame_tombol, text="Keluar", font=("Arial", 11, "bold"), bg="#E74C3C", fg="white", width=15, command=keluar)
btn_keluar.grid(row=0, column=1, padx=10)

# Label hasil
label_hasil = tk.Label(
    root,
    text="Hasil konversi akan ditampilkan di sini.",
    font=("Consolas", 11),
    bg="white",
    relief="groove",
    width=55,
    height=10,
    anchor="nw",
    justify="left"
)
label_hasil.pack(padx=10, pady=15)

# Jalankan program
root.mainloop()
