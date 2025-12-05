# aes_gui_rapi.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import tkinter.font as tkfont

# ---------------- AES TABLES & HELPERS (sama seperti versi Anda) ----------------
aes_sbox = [
    [0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
    [0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
    [0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
    [0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
    [0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
    [0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
    [0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
    [0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
    [0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
    [0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
    [0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
    [0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
    [0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
    [0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
    [0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
    [0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16],
]

rcon = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

def to_hex(b): return f"{b:02X}"
def to_bin8(b): return format(b, "08b")

def sub_byte(b):
    return aes_sbox[b >> 4][b & 0x0F]

def rot_word(w):
    return w[1:] + w[:1]

def sub_word(w):
    return [sub_byte(x) for x in w]

def gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a ^= 0x1B
        b >>= 1
    return p & 0xFF

def gmul_steps(a, b):
    lines = []
    a_val = a
    res = 0
    lines.append(f"Multiply {to_hex(a)} by {to_hex(b)}:")
    for i in range(8):
        if (b >> i) & 1:
            lines.append(f"  bit {i} of multiplier is 1 → XOR with {to_hex(a_val)}")
            res ^= a_val
        else:
            lines.append(f"  bit {i} of multiplier is 0 → skip")
        carry = (a_val & 0x80) != 0
        a_shift = (a_val << 1) & 0xFF
        if carry:
            a_shift ^= 0x1B
            lines.append(f"  shift: {to_hex(a_val)} <<1 -> {to_hex((a_val<<1)&0xFF)} then XOR 0x1B -> {to_hex(a_shift)} (carry)")
        else:
            lines.append(f"  shift: {to_hex(a_val)} <<1 -> {to_hex(a_shift)} (no carry)")
        a_val = a_shift
    lines.append(f"Result: {to_hex(res)}")
    return res, lines

def mix_single_column_steps(col):
    a0,a1,a2,a3 = col
    m02_a0, s02_a0 = gmul_steps(a0, 0x02)
    m02_a1, s02_a1 = gmul_steps(a1, 0x02)
    m02_a2, s02_a2 = gmul_steps(a2, 0x02)
    m02_a3, s02_a3 = gmul_steps(a3, 0x02)
    m03_a0 = m02_a0 ^ a0
    m03_a1 = m02_a1 ^ a1
    m03_a2 = m02_a2 ^ a2
    m03_a3 = m02_a3 ^ a3

    r0 = m02_a0 ^ m03_a1 ^ a2 ^ a3
    r1 = a0 ^ m02_a1 ^ m03_a2 ^ a3
    r2 = a0 ^ a1 ^ m02_a2 ^ m03_a3
    r3 = m03_a0 ^ a1 ^ a2 ^ m02_a3

    lines = []
    lines.append(f"MixColumn on column: {' '.join(to_hex(x) for x in col)}")
    lines.append(f" 02*{to_hex(a0)} -> {to_hex(m02_a0)}")
    lines += ["    "+ln for ln in s02_a0]
    lines.append(f" 02*{to_hex(a1)} -> {to_hex(m02_a1)}")
    lines += ["    "+ln for ln in s02_a1]
    lines.append(f" 02*{to_hex(a2)} -> {to_hex(m02_a2)}")
    lines += ["    "+ln for ln in s02_a2]
    lines.append(f" 02*{to_hex(a3)} -> {to_hex(m02_a3)}")
    lines += ["    "+ln for ln in s02_a3]
    lines.append(f"03*{to_hex(a1)} = 02*{to_hex(a1)} XOR {to_hex(a1)} -> {to_hex(m03_a1)}")
    lines.append(f"03*{to_hex(a2)} = 02*{to_hex(a2)} XOR {to_hex(a2)} -> {to_hex(m03_a2)}")
    lines.append(f"R0 = {to_hex(r0)} | R1 = {to_hex(r1)} | R2 = {to_hex(r2)} | R3 = {to_hex(r3)}")
    return [r0,r1,r2,r3], lines

# ---------------- KEY EXPANSION ----------------
def key_expansion_with_steps(key_hex):
    kb = [int(key_hex[i:i+2],16) for i in range(0,32,2)]
    key_mat = [[kb[r*4 + c] for c in range(4)] for r in range(4)]
    w = []
    # initial 4 words
    for c in range(4):
        w.append([key_mat[r][c] for r in range(4)])
    steps = []
    steps.append(("init", [word.copy() for word in w[:4]]))
    for i in range(4,44):
        temp = w[i-1].copy()
        detail = {"i":i, "temp_before": temp.copy(), "rot":None, "sub":None, "rcon":None, "new":None}
        if i % 4 == 0:
            rw = rot_word(temp)
            sw = sub_word(rw)
            sw_after = sw.copy()
            sw_after[0] ^= rcon[i//4]
            detail["rot"] = rw
            detail["sub"] = sw
            detail["rcon"] = sw_after
            temp = sw_after
        neww = [w[i-4][j] ^ temp[j] for j in range(4)]
        detail["new"] = neww
        w.append(neww)
        steps.append(("gen", detail))
    return w, steps, key_mat

def round_key_matrix_from_w(w, r):
    start = r*4
    rk = [[0]*4 for _ in range(4)]
    for c in range(4):
        word = w[start+c]
        for row in range(4):
            rk[row][c] = word[row]
    return rk

# ---------------- AES STEP FUNCTIONS ----------------
def pretty_mat(m):
    return "\n".join(" ".join(f"{m[r][c]:02X}" for c in range(4)) for r in range(4))

def add_round_key(state, rk, explain=False):
    out = [[(state[r][c] ^ rk[r][c]) & 0xFF for c in range(4)] for r in range(4)]
    lines = []
    if explain:
        lines.append("AddRoundKey (per byte XOR):")
        for r in range(4):
            for c in range(4):
                a = state[r][c]; b = rk[r][c]; xr = a ^ b
                lines.append(f" {to_hex(a)} ({to_bin8(a)}) XOR {to_hex(b)} ({to_bin8(b)}) = {to_hex(xr)} ({to_bin8(xr)})")
    return out, lines

def sub_bytes_with_steps(state):
    out = [[0]*4 for _ in range(4)]
    lines = ["SubBytes mapping (S-Box lookup):"]
    for r in range(4):
        for c in range(4):
            b = state[r][c]
            s = aes_sbox[b >> 4][b & 0x0F]
            out[r][c] = s
            lines.append(f" {to_hex(b)} -> SBOX[{b>>4}][{b&0x0F:X}] = {to_hex(s)}")
    return out, lines

def shift_rows_with_steps(state):
    out = [[0]*4 for _ in range(4)]
    lines = ["ShiftRows (row shifts):"]
    for r in range(4):
        row = state[r]
        shifted = row[r:] + row[:r]
        for c in range(4): out[r][c] = shifted[c]
        lines.append(f" Row {r}: " + " ".join(to_hex(x) for x in row) + " -> " + " ".join(to_hex(x) for x in shifted))
    return out, lines

def mix_columns_with_steps(state):
    out = [[0]*4 for _ in range(4)]
    lines = ["MixColumns (detailed GF steps):"]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        mixed, mlines = mix_single_column_steps(col)
        for r in range(4): out[r][c] = mixed[r]
        lines.append(f" Column {c}: {' '.join(to_hex(x) for x in col)} -> {' '.join(to_hex(x) for x in mixed)}")
        lines += ["   "+ln for ln in mlines]
    return out, lines

# ---------------- GUI / UX helpers ----------------
def style_text_widget(txt):
    # Configure tags for colors and fonts
    txt.tag_config("header", font=mono_bold, foreground="#0F62FE")   # vivid blue
    txt.tag_config("sub", font=mono_bold, foreground="#6F42C1")      # purple
    txt.tag_config("code", font=mono, foreground="#111111")         # dark
    txt.tag_config("error", font=mono_bold, foreground="#D32F2F")   # red
    txt.tag_config("muted", font=mono, foreground="#555555")

def insertln(txt, s, tag="code"):
    txt.insert(tk.END, s + "\n", tag)
    txt.see(tk.END)

def clear_output():
    output.configure(state=tk.NORMAL)
    output.delete(1.0, tk.END)
    output.configure(state=tk.DISABLED)

def copy_ciphertext():
    txt = ciphertext_var.get()
    if not txt:
        messagebox.showinfo("Salin", "Belum ada ciphertext untuk disalin.")
        return
    root.clipboard_clear()
    root.clipboard_append(txt)
    messagebox.showinfo("Salin", "Ciphertext telah disalin ke clipboard.")

# ---------------- Main process (menggunakan format yang detil) ----------------
def run_full_process():
    key = entry_key.get()
    plain = entry_plain.get()

    # Validate
    if len(key) != 16 or len(plain) != 16:
        messagebox.showerror("Input error", "Key dan Plaintext harus 16 karakter ASCII masing-masing.")
        return

    clear_output()
    output.configure(state=tk.NORMAL)
    insertln(output, "=== LANGKAH 1: Konversi ASCII → HEX → BIN ===", "header")
    key_hex = "".join(f"{ord(c):02X}" for c in key)
    plain_hex = "".join(f"{ord(c):02X}" for c in plain)
    insertln(output, f"Plaintext ASCII : {plain}", "muted")
    insertln(output, f"Plaintext HEX   : {plain_hex}", "code")
    pbytes = [int(plain_hex[i:i+2],16) for i in range(0,32,2)]
    for i,b in enumerate(pbytes):
        insertln(output, f"P[{i}] = {to_hex(b)}₁₆ = {to_bin8(b)}₂", "code")
    insertln(output, "", "code")
    insertln(output, f"Cipher Key ASCII: {key}", "muted")
    insertln(output, f"Cipher Key HEX  : {key_hex}", "code")
    kbytes = [int(key_hex[i:i+2],16) for i in range(0,32,2)]
    for i,b in enumerate(kbytes):
        insertln(output, f"K[{i}] = {to_hex(b)}₁₆ = {to_bin8(b)}₂", "code")
    insertln(output, "", "code")

    # LANGKAH 2: XOR per byte (Plain ⊕ Key)
    insertln(output, "=== LANGKAH 2: XOR Plaintext ⊕ CipherKey (per byte) ===", "header")
    insertln(output, "Idx | Plain HEX (bin)         | Key HEX (bin)          | XOR -> HEX (bin)", "sub")
    insertln(output, "-"*80, "muted")
    xor_res = []
    for i in range(16):
        a = pbytes[i]; b = kbytes[i]; xr = a ^ b
        insertln(output, f"{i:02d}  | {to_hex(a)} ({to_bin8(a)}) | {to_hex(b)} ({to_bin8(b)}) | {to_hex(xr)} ({to_bin8(xr)})", "code")
        xor_res.append(xr)
    insertln(output, "", "code")

    # LANGKAH 3: Key expansion with steps
    insertln(output, "=== LANGKAH 3: PEMBANGKITAN KUNCI (Key Expansion) ===", "header")
    w, steps, key_mat = key_expansion_with_steps(key_hex)
    insertln(output, "Initial Key matrix (row-major):", "sub")
    insertln(output, pretty_mat(key_mat), "code")
    insertln(output, "", "code")
    insertln(output, "Round keys K0..K10:", "sub")
    for r in range(11):
        rk = round_key_matrix_from_w(w, r)
        insertln(output, f"K{r}:\n{pretty_mat(rk)}\n", "code")

    insertln(output, "Detail Key Expansion (RotWord / SubWord / Rcon / NewWord):", "sub")
    for s in steps:
        if s[0] == "init":
            init = s[1]
            for idx, ww in enumerate(init):
                insertln(output, f"W{idx}: " + " ".join(to_hex(b) for b in ww), "code")
            insertln(output, "", "code")
        else:
            d = s[1]; i = d["i"]
            insertln(output, f"i={i} temp_before: " + " ".join(to_hex(b) for b in d["temp_before"]), "code")
            if d["rot"] is not None:
                insertln(output, "  RotWord: " + " ".join(to_hex(b) for b in d["rot"]), "code")
                insertln(output, "  SubWord (S-Box lookups):", "muted")
                for j, sb in enumerate(d["sub"]):
                    b = d["rot"][j]
                    insertln(output, f"    byte {j}: {to_hex(b)} -> row {b>>4}, col {b&0x0F:X} -> {to_hex(sb)}", "code")
                insertln(output, "  After Rcon XOR (first byte): " + " ".join(to_hex(b) for b in d["rcon"]), "code")
            insertln(output, "  New word (w{}): ".format(i) + " ".join(to_hex(b) for b in d["new"]), "code")
            insertln(output, "", "code")

    # Build initial state (row-major)
    state = [[pbytes[r*4 + c] for c in range(4)] for r in range(4)]
    insertln(output, "=== INITIAL STATE (row-major) ===", "header")
    insertln(output, pretty_mat(state), "code")
    insertln(output, "", "code")

    # Round 0 AddRoundKey
    insertln(output, "=== ROUND 0: Initial AddRoundKey ===", "header")
    rk0 = round_key_matrix_from_w(w, 0)
    insertln(output, "Round Key K0:", "sub")
    insertln(output, pretty_mat(rk0), "code")
    state, add_lines = add_round_key(state, rk0, explain=True)
    for ln in add_lines:
        insertln(output, ln, "code")
    insertln(output, "\nState after AddRoundKey:\n" + pretty_mat(state), "code")

    # Rounds 1..9
    for r in range(1, 10):
        insertln(output, f"\n========== ROUND {r} ==========", "header")
        sb_state, sb_lines = sub_bytes_with_steps(state)
        insertln(output, "🔹 SubBytes:", "sub")
        for ln in sb_lines: insertln(output, ln, "code")
        insertln(output, "State after SubBytes:\n" + pretty_mat(sb_state), "code")

        sr_state, sr_lines = shift_rows_with_steps(sb_state)
        insertln(output, "🔹 ShiftRows:", "sub")
        for ln in sr_lines: insertln(output, ln, "code")
        insertln(output, "State after ShiftRows:\n" + pretty_mat(sr_state), "code")

        mc_state, mc_lines = mix_columns_with_steps(sr_state)
        insertln(output, "🔹 MixColumns:", "sub")
        for ln in mc_lines: insertln(output, ln, "code")
        insertln(output, "State after MixColumns:\n" + pretty_mat(mc_state), "code")

        rk = round_key_matrix_from_w(w, r)
        insertln(output, f"Round Key K{r}:\n{pretty_mat(rk)}", "code")
        state, add_lines = add_round_key(mc_state, rk, explain=True)
        insertln(output, "After AddRoundKey:", "sub")
        for ln in add_lines: insertln(output, ln, "code")
        insertln(output, "State after AddRoundKey:\n" + pretty_mat(state), "code")

    # Round 10 (no MixColumns)
    insertln(output, "\n========== ROUND 10 ==========", "header")
    sb_state, sb_lines = sub_bytes_with_steps(state)
    insertln(output, "🔹 SubBytes:", "sub")
    for ln in sb_lines: insertln(output, ln, "code")
    sr_state, sr_lines = shift_rows_with_steps(sb_state)
    insertln(output, "🔹 ShiftRows:", "sub")
    for ln in sr_lines: insertln(output, ln, "code")
    rk10 = round_key_matrix_from_w(w, 10)
    insertln(output, f"Round Key K10:\n{pretty_mat(rk10)}", "code")
    state, add_lines = add_round_key(sr_state, rk10, explain=True)
    insertln(output, "After AddRoundKey (Final):", "sub")
    for ln in add_lines: insertln(output, ln, "code")
    insertln(output, "\nFinal Ciphertext state:\n" + pretty_mat(state), "code")

    # Final ciphertext (row-major)
    chex = "".join(to_hex(state[r][c]) for r in range(4) for c in range(4))
    insertln(output, f"\n=== CIPHERTEXT (HEX, row-major): {chex} ===", "header")
    ciphertext_var.set(chex)

    output.configure(state=tk.DISABLED)
    # focus to show result
    output.see(tk.END)

# ---------------- Build Tkinter UI ----------------
root = tk.Tk()
root.title("KRIPTOGRAFI AES")
root.geometry("1100x760")
root.minsize(980, 640)

# Fonts
mono = tkfont.Font(family="Consolas", size=10)
mono_bold = tkfont.Font(family="Consolas", size=10, weight="bold")
heading_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")

# Style ttk
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background="#F6F8FB")
style.configure("Title.TLabel", font=heading_font, background="#F6F8FB", foreground="#0F172A")
style.configure("TLabel", background="#F6F8FB", foreground="#0F172A")
style.configure("Accent.TButton", background="#0F62FE", foreground="white", font=("Segoe UI", 10, "bold"))
style.map("Accent.TButton", background=[("active", "#0353e9")])
style.configure("Outline.TButton", background="#E6EEF8", foreground="#0F62FE")
style.configure("Entry.TEntry", padding=6)

# Top frame
top = ttk.Frame(root, padding=(12,12))
top.pack(fill=tk.X)

ttk.Label(top, text="Kriptografi dengan AES GENERATE KEY - ENKRISI PLAINTEXT", style="Title.TLabel").pack(side=tk.LEFT, padx=(6,12))
ttk.Label(top, text="LIHAT DAN PAHAMI", foreground="#6B6B6B").pack(side=tk.LEFT)

# Input frame
frm = ttk.Frame(root, padding=(12,8))
frm.pack(fill=tk.X, padx=12, pady=(6,0))

ttk.Label(frm, text="Cipher Key (16 ASCII chars):").grid(row=0, column=0, sticky="w")
entry_key = ttk.Entry(frm, width=36, style="Entry.TEntry")
entry_key.grid(row=0, column=1, padx=8, sticky="w")

ttk.Label(frm, text="Plaintext (16 ASCII chars):").grid(row=1, column=0, sticky="w", pady=(6,0))
entry_plain = ttk.Entry(frm, width=36, style="Entry.TEntry")
entry_plain.grid(row=1, column=1, padx=8, sticky="w", pady=(6,0))

# Buttons and actions
btn_frm = ttk.Frame(frm)
btn_frm.grid(row=0, column=2, rowspan=2, padx=16, sticky="n")

run_btn = ttk.Button(btn_frm, text="Run (Detail)", style="Accent.TButton", command=run_full_process)
run_btn.pack(fill=tk.X, pady=(0,6))
clear_btn = ttk.Button(btn_frm, text="Clear Output", style="Outline.TButton", command=clear_output)
clear_btn.pack(fill=tk.X, pady=(0,6))

# Example presets
def fill_example():
    entry_key.delete(0, tk.END); entry_plain.delete(0, tk.END)
    entry_key.insert(0, "Text Kunci")   # 16 chars
    entry_plain.insert(0, "Plain Text")  # 16 chars

preset_btn = ttk.Button(btn_frm, text="Isi contoh", command=fill_example)
preset_btn.pack(fill=tk.X, pady=(0,6))

# Ciphertext display & copy
cipher_frm = ttk.Frame(frm)
cipher_frm.grid(row=2, column=0, columnspan=3, pady=(12,0), sticky="w")
ttk.Label(cipher_frm, text="Ciphertext (HEX):").pack(side=tk.LEFT)
ciphertext_var = tk.StringVar()
cipher_lbl = ttk.Entry(cipher_frm, textvariable=ciphertext_var, width=60, state="readonly")
cipher_lbl.pack(side=tk.LEFT, padx=(8,6))
cpy_btn = ttk.Button(cipher_frm, text="Copy", command=copy_ciphertext)
cpy_btn.pack(side=tk.LEFT)

# Output area (scrolled)
out_frm = ttk.Frame(root, padding=(12,8))
out_frm.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

output = scrolledtext.ScrolledText(out_frm, wrap=tk.WORD, font=mono)
output.pack(fill=tk.BOTH, expand=True)
style_text_widget(output)
output.configure(state=tk.DISABLED)

# Footer
foot = ttk.Frame(root)
foot.pack(fill=tk.X, padx=12, pady=(0,12))
ttk.Label(foot, text="Menunjukkan langkah AES (128-bit) secara rinci.", foreground="#444444").pack(side=tk.LEFT)

# Start with example values
fill_example()

root.mainloop()
