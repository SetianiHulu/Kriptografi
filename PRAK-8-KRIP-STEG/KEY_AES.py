import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

# =====================================================
#  AES — SBOX dan RCON
# =====================================================

SBOX = [
0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]

RCON = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

# =====================================================
#  UTIL
# =====================================================

def to_hex(b): return f"{b:02X}"

def pad16(s): return s[:16].ljust(16)

def text_to_bytes(s):
    s16 = pad16(s)
    return [ord(c) for c in s16]

def bytes_to_matrix_colmajor(bts):
    m = [[0]*4 for _ in range(4)]
    for col in range(4):
        for row in range(4):
            m[row][col] = bts[col*4 + row]
    return m

def matrix_to_hex(m):
    return "\n".join(
        " ".join(to_hex(m[r][c]) for c in range(4)) for r in range(4)
    )

def words_from_key_bytes(key_bytes):
    return [[key_bytes[4*c + r] for r in range(4)] for c in range(4)]

def rot_word(w): return w[1:] + w[:1]
def sub_word(w): return [SBOX[b] for b in w]
def xor_words(a,b): return [a[i]^b[i] for i in range(4)]

# GF math
def gmul(a,b):
    res = 0
    for i in range(8):
        if b & 1:
            res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return res

# AES transforms
def mix_single_column(col):
    a0,a1,a2,a3 = col
    return [
        gmul(a0,2) ^ gmul(a1,3) ^ gmul(a2,1) ^ gmul(a3,1),
        gmul(a0,1) ^ gmul(a1,2) ^ gmul(a2,3) ^ gmul(a3,1),
        gmul(a0,1) ^ gmul(a1,1) ^ gmul(a2,2) ^ gmul(a3,3),
        gmul(a0,3) ^ gmul(a1,1) ^ gmul(a2,1) ^ gmul(a3,2),
    ]

def mix_columns(state):
    out = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        res = mix_single_column(col)
        for r in range(4):
            out[r][c] = res[r]
    return out

def sub_bytes(state):
    return [[SBOX[state[r][c]] for c in range(4)] for r in range(4)]

def shift_rows(state):
    out = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            out[r][c] = state[r][(c+r)%4]
    return out

def add_round_key(state, key):
    return [[state[r][c]^key[r][c] for c in range(4)] for r in range(4)]

# =====================================================
#  KEY EXPANSION
# =====================================================

def key_expansion_from_keytext(keytext):
    key_bytes = text_to_bytes(keytext)
    w = words_from_key_bytes(key_bytes)

    log = []
    log.append("=== KEY EXPANSION (AES-128) ===")
    log.append("Initial Words:")
    for i in range(4):
        log.append(f"w{i}: " + " ".join(to_hex(x) for x in w[i]))
    log.append("")

    for i in range(4,44):
        temp = w[i-1].copy()
        if i % 4 == 0:
            log.append(f"[Round {i//4}] w{i} generation:")
            log.append("Before RotWord: " + " ".join(to_hex(x) for x in temp))
            temp = rot_word(temp)
            log.append("RotWord     -> " + " ".join(to_hex(x) for x in temp))
            temp = sub_word(temp)
            log.append("SubWord     -> " + " ".join(to_hex(x) for x in temp))
            rcon_word = [RCON[i//4],0,0,0]
            log.append("Rcon        -> " + " ".join(to_hex(x) for x in rcon_word))
            temp = xor_words(temp, rcon_word)
            log.append("XOR Rcon    -> " + " ".join(to_hex(x) for x in temp))
        neww = xor_words(w[i-4], temp)
        w.append(neww)
        log.append(f"w{i}: " + " ".join(to_hex(x) for x in neww))
        log.append("")

    # convert to 11 round keys
    round_keys = []
    for r in range(11):
        segment = w[r*4:r*4+4]
        m = [[segment[c][r2] for c in range(4)] for r2 in range(4)]
        round_keys.append(m)

    return log, round_keys

# =====================================================
#  AES ENCRYPTION WITH LOGGING
# =====================================================

def aes_encrypt_and_log(pt_text, key_text):
    log = []
    pt = pad16(pt_text)
    key = pad16(key_text)

    pt_bytes = text_to_bytes(pt)
    key_bytes = text_to_bytes(key)

    # Matrices
    pt_mat = bytes_to_matrix_colmajor(pt_bytes)
    key_mat = bytes_to_matrix_colmajor(key_bytes)

    log.append("=== LANGKAH 1: KONVERSI ===")
    log.append("Plaintext HEX : " + " ".join(to_hex(b) for b in pt_bytes))
    log.append("Plaintext Matrix:\n" + matrix_to_hex(pt_mat))
    log.append("")
    log.append("CipherKey HEX : " + " ".join(to_hex(b) for b in key_bytes))
    log.append("CipherKey Matrix:\n" + matrix_to_hex(key_mat))
    log.append("")

    # Key expansion
    keylog, round_keys = key_expansion_from_keytext(key)
    log.extend(keylog)

    # Initial AddRoundKey
    log.append("=== ROUND 0 (AddRoundKey) ===")
    state = add_round_key(pt_mat, round_keys[0])
    log.append(matrix_to_hex(state))
    log.append("")

    # 9 rounds AES
    for r in range(1,10):
        log.append(f"=== ROUND {r} ===")
        state = sub_bytes(state)
        log.append("SubBytes:\n" + matrix_to_hex(state))
        state = shift_rows(state)
        log.append("ShiftRows:\n" + matrix_to_hex(state))
        state = mix_columns(state)
        log.append("MixColumns:\n" + matrix_to_hex(state))
        state = add_round_key(state, round_keys[r])
        log.append(f"AddRoundKey K{r}:\n" + matrix_to_hex(state))
        log.append("")

    # Final round
    log.append("=== FINAL ROUND (10) ===")
    state = sub_bytes(state)
    log.append("SubBytes:\n" + matrix_to_hex(state))
    state = shift_rows(state)
    log.append("ShiftRows:\n" + matrix_to_hex(state))
    state = add_round_key(state, round_keys[10])
    log.append("AddRoundKey K10:\n" + matrix_to_hex(state))
    log.append("")

    # Output ciphertext
    cipher = []
    for c in range(4):
        for r in range(4):
            cipher.append(state[r][c])

    cipher_hex = " ".join(to_hex(x) for x in cipher)
    cipher_ascii = "".join(chr(x) for x in cipher)

    log.append("=== CIPHERTEXT (HEX) ===")
    log.append(cipher_hex)
    log.append("")

    return "\n".join(log), cipher_hex, cipher_ascii

# =====================================================
#  GUI — ELEGANT DARK THEME
# =====================================================

root = tk.Tk()
root.title("AES-128 ENCRYPTION — KEY EXPANSION & FULL PROCESS")
root.geometry("1300x750")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
style.configure("TEntry", padding=6, font=("Consolas", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)

top_frame = ttk.Frame(root)
top_frame.pack(pady=15)

ttk.Label(top_frame, text="Plaintext:").grid(row=0, column=0, sticky="w")
entry_pt = ttk.Entry(top_frame, width=60)
entry_pt.grid(row=0, column=1, padx=10)

ttk.Label(top_frame, text="Cipher Key:").grid(row=1, column=0, sticky="w")
entry_key = ttk.Entry(top_frame, width=60)
entry_key.grid(row=1, column=1, padx=10)

def run_encrypt():
    pt = entry_pt.get()
    key = entry_key.get()

    if not pt or not key:
        messagebox.showerror("Error", "Masukkan Plaintext dan Key!")
        return

    log, cipher_hex, cipher_ascii = aes_encrypt_and_log(pt, key)

    txt_log.delete("1.0", tk.END)
    txt_log.insert(tk.END, log)

    lbl_cipher_hex.config(text=cipher_hex)
    lbl_cipher_ascii.config(text=cipher_ascii)

btn_encrypt = ttk.Button(root, text="Mulai Enkripsi AES-128", command=run_encrypt)
btn_encrypt.pack(pady=10)

# Log output
txt_log = scrolledtext.ScrolledText(root, width=150, height=25, background="#0d0d0d",
                                    foreground="#00ff99", insertbackground="white",
                                    font=("Consolas", 10))
txt_log.pack(pady=10)

# Cipher result box
cipher_frame = ttk.Frame(root)
cipher_frame.pack(pady=10)

ttk.Label(cipher_frame, text="Hasil Ciphertext (HEX):").grid(row=0, column=0, sticky="w")
lbl_cipher_hex = ttk.Label(cipher_frame, text="", foreground="#00e6ff")
lbl_cipher_hex.grid(row=0, column=1, padx=10)

ttk.Label(cipher_frame, text="Ciphertext (ASCII):").grid(row=1, column=0, sticky="w")
lbl_cipher_ascii = ttk.Label(cipher_frame, text="", foreground="#ffcc00")
lbl_cipher_ascii.grid(row=1, column=1, padx=10)

root.mainloop()
