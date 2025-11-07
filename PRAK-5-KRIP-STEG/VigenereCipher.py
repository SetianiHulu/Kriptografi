import string
import tkinter as tk
from tkinter import ttk, messagebox

class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()
        self.alphabet = string.ascii_uppercase

    def _format_key(self, text):
        key_extended = ""
        i = 0
        for char in text:
            if char.upper() in self.alphabet:
                key_extended += self.key[i % len(self.key)]
                i += 1
            else:
                key_extended += char
        return key_extended

    def encrypt_step(self, text):
        text = text.upper()
        key = self._format_key(text)
        steps = []
        result = ""

        for t, k in zip(text, key):
            if t in self.alphabet:
                enc = self.alphabet[(self.alphabet.index(t) + self.alphabet.index(k)) % 26]
                steps.append(f"{t} + {k} → {enc}")
                result += enc
            else:
                steps.append(f"{t} (tidak diubah)")
                result += t
        return result, steps

    def decrypt_step(self, text):
        text = text.upper()
        key = self._format_key(text)
        steps = []
        result = ""

        for t, k in zip(text, key):
            if t in self.alphabet:
                dec = self.alphabet[(self.alphabet.index(t) - self.alphabet.index(k)) % 26]
                steps.append(f"{t} - {k} → {dec}")
                result += dec
            else:
                steps.append(f"{t} (tidak diubah)")
                result += t
        return result, steps


# ========== GUI Dinamis ==========
def proses(mode):
    key = entry_key.get().strip()
    text = entry_text.get("1.0", tk.END).strip()

    if not key or not text:
        messagebox.showwarning("Peringatan", "Harap isi teks dan kunci terlebih dahulu!")
        return

    cipher = VigenereCipher(key)

    if mode == "Enkripsi":
        hasil, langkah = cipher.encrypt_step(text)
    else:
        hasil, langkah = cipher.decrypt_step(text)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, hasil)

    step_text.delete("1.0", tk.END)
    for s in langkah:
        step_text.insert(tk.END, s + "\n")


# ======= Desain GUI =======
root = tk.Tk()
root.title("🔐 Vigenère Cipher - Dinamis")
root.geometry("650x600")
root.configure(bg="#E9F2FF")
root.resizable(False, False)

# Judul
judul = tk.Label(root, text="Vigenère Cipher", font=("Helvetica", 20, "bold"), bg="#E9F2FF", fg="#1B3C73")
judul.pack(pady=10)

# Frame input
frame_input = ttk.Frame(root)
frame_input.pack(pady=10)

ttk.Label(frame_input, text="Kunci:").grid(row=0, column=0, padx=5, pady=5)
entry_key = ttk.Entry(frame_input, width=40)
entry_key.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Teks:").grid(row=1, column=0, padx=5, pady=5)
entry_text = tk.Text(frame_input, height=4, width=50)
entry_text.grid(row=1, column=1, padx=5, pady=5)

# Tombol
frame_btn = ttk.Frame(root)
frame_btn.pack(pady=10)
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6)

ttk.Button(frame_btn, text="🔒 Enkripsi", command=lambda: proses("Enkripsi")).grid(row=0, column=0, padx=10)
ttk.Button(frame_btn, text="🔓 Dekripsi", command=lambda: proses("Dekripsi")).grid(row=0, column=1, padx=10)
ttk.Button(frame_btn, text="❌ Keluar", command=root.quit).grid(row=0, column=2, padx=10)

# Hasil
ttk.Label(root, text="Hasil:", font=("Helvetica", 10, "bold"), background="#E9F2FF").pack(pady=5)
output_text = tk.Text(root, height=4, width=70, font=("Courier New", 10))
output_text.pack(pady=5)

# Proses langkah
ttk.Label(root, text="Langkah Proses:", font=("Helvetica", 10, "bold"), background="#E9F2FF").pack(pady=5)
step_text = tk.Text(root, height=10, width=70, font=("Consolas", 9), bg="#F9FAFB", fg="#333")
step_text.pack(pady=5)

# Footer
footer = tk.Label(root, text="SETIANII❤️", bg="#E9F2FF", fg="#555", font=("Arial", 9))
footer.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
