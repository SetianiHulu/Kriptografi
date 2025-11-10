import tkinter as tk
from tkinter import ttk

# Fungsi konversi nilai ke huruf dan bobot
def konversi_nilai(nilai):
    if 81 <= nilai <= 100:
        return "A", 4
    elif 76 <= nilai <= 80:
        return "B+", 3.5
    elif 71 <= nilai <= 75:
        return "B", 3
    elif 66 <= nilai <= 70:
        return "C+", 2.5
    elif 56 <= nilai <= 65:
        return "C", 2
    elif 46 <= nilai <= 55:
        return "D", 1
    else:
        return "E", 0

# Fungsi hitung nilai akhir
def hitung():
    try:
        sikap = float(entry_sikap.get())
        tugas = float(entry_tugas.get())
        uts = float(entry_uts.get())
        uas = float(entry_uas.get())

        # Hitung total
        total = (sikap * 0.10) + (tugas * 0.30) + (uts * 0.25) + (uas * 0.35)
        huruf, bobot = konversi_nilai(total)
        ket = "Lulus" if total >= 56 else "Tidak Lulus"

        # Bersihkan tabel lama
        for item in table.get_children():
            table.delete(item)

        # Masukkan hasil ke tabel
        table.insert("", "end", values=(f"{total:.2f}", huruf, bobot, ket))

    except ValueError:
        for item in table.get_children():
            table.delete(item)
        table.insert("", "end", values=("Input tidak valid", "-", "-", "-"))

# --- GUI Form ---
root = tk.Tk()
root.title("Kalkulator Nilai Akhir Akademik")
root.geometry("500x350")
root.resizable(False, False)

# Bagian input
frame_input = tk.Frame(root, pady=10)
frame_input.pack()

tk.Label(frame_input, text="Nilai Sikap/Keaktifan:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_sikap = tk.Entry(frame_input, width=10)
entry_sikap.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Nilai Tugas:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_tugas = tk.Entry(frame_input, width=10)
entry_tugas.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Nilai UTS:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_uts = tk.Entry(frame_input, width=10)
entry_uts.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Nilai UAS:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_uas = tk.Entry(frame_input, width=10)
entry_uas.grid(row=3, column=1, padx=10, pady=5)

# Tombol hitung
btn_hitung = tk.Button(root, text="Hitung Nilai Akhir", command=hitung, bg="lightblue", width=20)
btn_hitung.pack(pady=10)

# Tabel hasil
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

table = ttk.Treeview(frame_table, columns=("total", "huruf", "bobot", "ket"), show="headings", height=3)
table.heading("total", text="Nilai Akhir")
table.heading("huruf", text="Nilai Huruf")
table.heading("bobot", text="Bobot")
table.heading("ket", text="Keterangan")

table.column("total", width=100, anchor="center")
table.column("huruf", width=100, anchor="center")
table.column("bobot", width=100, anchor="center")
table.column("ket", width=120, anchor="center")

table.pack()

root.mainloop()
