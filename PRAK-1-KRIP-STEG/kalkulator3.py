import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------
# FORM LATIHAN 1: Operasi Aritmatika
# ---------------------------
def form_latihan1(container, back_to_menu):
    frame = tk.Frame(container)

    tk.Label(frame, text="Latihan 1: Operasi Aritmatika", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(frame, text="Angka 1:").pack()
    entry_a = tk.Entry(frame)
    entry_a.pack()

    tk.Label(frame, text="Angka 2:").pack()
    entry_b = tk.Entry(frame)
    entry_b.pack()

    hasil = tk.Label(frame, text="", font=("Arial", 11))
    hasil.pack(pady=10)

    def hitung():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            teks = (
                f"Penjumlahan: {a+b}\n"
                f"Pengurangan: {a-b}\n"
                f"Perkalian: {a*b}\n"
                f"Pembagian: {a/b if b!=0 else 'Error (bagi 0)'}"
            )
            hasil.config(text=teks)
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka!")

    tk.Button(frame, text="Hitung", command=hitung).pack(pady=5)
    tk.Button(frame, text="Kembali ke Menu", command=back_to_menu, bg="lightgray").pack(pady=10)

    return frame

# ---------------------------
# FORM LATIHAN 2: Kalkulator
# ---------------------------
def form_latihan2(container, back_to_menu):
    frame = tk.Frame(container)

    tk.Label(frame, text="Latihan 2: Kalkulator Sederhana", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(frame, text="Angka 1:").pack()
    entry1 = tk.Entry(frame)
    entry1.pack()

    tk.Label(frame, text="Operator (+, -, *, /):").pack()
    entry_op = tk.Entry(frame)
    entry_op.pack()

    tk.Label(frame, text="Angka 2:").pack()
    entry2 = tk.Entry(frame)
    entry2.pack()

    hasil = tk.Label(frame, text="", font=("Arial", 11))
    hasil.pack(pady=10)

    def hitung():
        try:
            a = float(entry1.get())
            b = float(entry2.get())
            op = entry_op.get()

            if op == '+':
                res = a + b
            elif op == '-':
                res = a - b
            elif op == '*':
                res = a * b
            elif op == '/':
                res = a / b if b != 0 else "Error (bagi 0)"
            else:
                res = "Operator tidak valid!"

            hasil.config(text=f"Hasil: {res}")
        except ValueError:
            messagebox.showerror("Error", "Input tidak valid!")

    tk.Button(frame, text="Hitung", command=hitung).pack(pady=5)
    tk.Button(frame, text="Kembali ke Menu", command=back_to_menu, bg="lightgray").pack(pady=10)

    return frame

# ---------------------------
# FORM LATIHAN 3: Nilai Akhir
# ---------------------------
def form_latihan3(container, back_to_menu):
    frame = tk.Frame(container)

    tk.Label(frame, text="Latihan 3: Hitung Nilai Akhir Akademik", font=("Arial", 12, "bold")).pack(pady=10)

    labels = ["Sikap/Keaktifan (%)", "Tugas (%)", "UTS (%)", "UAS (%)"]
    entries = []

    for lbl in labels:
        tk.Label(frame, text=lbl).pack()
        e = tk.Entry(frame)
        e.pack()
        entries.append(e)

    hasil_table = ttk.Treeview(frame, columns=("total", "huruf", "bobot", "ket"), show="headings", height=3)
    hasil_table.heading("total", text="Nilai Akhir")
    hasil_table.heading("huruf", text="Huruf")
    hasil_table.heading("bobot", text="Bobot")
    hasil_table.heading("ket", text="Keterangan")

    for col in ("total", "huruf", "bobot", "ket"):
        hasil_table.column(col, width=100, anchor="center")
    hasil_table.pack(pady=10)

    def konversi_nilai(nilai):
        if 81 <= nilai <= 100: return "A", 4
        elif 76 <= nilai <= 80: return "B+", 3.5
        elif 71 <= nilai <= 75: return "B", 3
        elif 66 <= nilai <= 70: return "C+", 2.5
        elif 56 <= nilai <= 65: return "C", 2
        elif 46 <= nilai <= 55: return "D", 1
        else: return "E", 0

    def hitung():
        try:
            sikap = float(entries[0].get())
            tugas = float(entries[1].get())
            uts = float(entries[2].get())
            uas = float(entries[3].get())

            total = (sikap*0.10) + (tugas*0.30) + (uts*0.25) + (uas*0.35)
            huruf, bobot = konversi_nilai(total)
            ket = "Lulus" if total >= 56 else "Tidak Lulus"

            for item in hasil_table.get_children():
                hasil_table.delete(item)
            hasil_table.insert("", "end", values=(f"{total:.2f}", huruf, bobot, ket))

        except ValueError:
            messagebox.showerror("Error", "Input harus angka!")

    tk.Button(frame, text="Hitung Nilai Akhir", command=hitung, bg="lightblue").pack(pady=5)
    tk.Button(frame, text="Kembali ke Menu", command=back_to_menu, bg="lightgray").pack(pady=10)

    return frame

# ---------------------------
# MAIN APP
# ---------------------------
def main():
    root = tk.Tk()
    root.title("Aplikasi Multi Latihan")
    root.geometry("500x400")

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # Frame menu utama
    menu_frame = tk.Frame(container)
    tk.Label(menu_frame, text="MENU UTAMA", font=("Arial", 14, "bold")).pack(pady=20)

    def show_form(form_func):
        menu_frame.pack_forget()
        form = form_func(container, back_to_menu)
        form.pack(fill="both", expand=True)

        def kembali():
            form.pack_forget()
            menu_frame.pack(fill="both", expand=True)

        # override fungsi kembali ke menu
        nonlocal back_to_menu
        back_to_menu = kembali

    back_to_menu = lambda: None  # default

    tk.Button(menu_frame, text="Latihan 1: Aritmatika", width=30, command=lambda: show_form(form_latihan1)).pack(pady=5)
    tk.Button(menu_frame, text="Latihan 2: Kalkulator", width=30, command=lambda: show_form(form_latihan2)).pack(pady=5)
    tk.Button(menu_frame, text="Latihan 3: Nilai Akhir", width=30, command=lambda: show_form(form_latihan3)).pack(pady=5)

    menu_frame.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
