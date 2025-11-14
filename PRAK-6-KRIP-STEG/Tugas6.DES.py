import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from functools import partial

# =========================
# DES TABLES (complete)
# =========================

PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

IP = [
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7
]

IP_INV = [
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
]

E = [
    32,1,2,3,4,5,
    4,5,6,7,8,9,
    8,9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

P = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

S_BOX = [
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    ],
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
    ],
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
    ],
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
    ],
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
    ],
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
    ],
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
    ],
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
    ]
]

ROTATIONS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

# =========================
# Helper bit functions
# =========================

def str_to_bitstr(s: str) -> str:
    return ''.join(f"{ord(c):08b}" for c in s)

def bytes_to_bitstr(b: bytes) -> str:
    return ''.join(f"{byte:08b}" for byte in b)

def bitstr_to_bytes(bs: str) -> bytes:
    out = bytearray()
    for i in range(0, len(bs), 8):
        out.append(int(bs[i:i+8], 2))
    return bytes(out)

def permute(bs: str, table: list) -> str:
    return ''.join(bs[i-1] for i in table)

def left_rotate(bs: str, n: int) -> str:
    n = n % len(bs)
    return bs[n:] + bs[:n]

def xor_bits(a: str, b: str) -> str:
    return ''.join('0' if a[i]==b[i] else '1' for i in range(len(a)))

def sbox_outputs(bits48: str):
    """Return list of 8 integers (0..15) and also combined 32-bit string"""
    outs = []
    combined = ""
    for i in range(8):
        block = bits48[i*6:(i+1)*6]
        row = (int(block[0]) << 1) | int(block[5])
        col = int(block[1:5], 2)
        val = S_BOX[i][row][col]
        outs.append(val)
        combined += f"{val:04b}"
    return outs, combined

def pkcs7_pad_bytes(b: bytes) -> bytes:
    pad = 8 - (len(b) % 8)
    if pad == 0: pad = 8
    return b + bytes([pad])*pad

# =========================
# Key schedule: PC-1, rotations, PC-2 (with C/D tracking)
# =========================

def generate_subkeys_and_CDs(key_bytes: bytes):
    # ensure 8 bytes
    if len(key_bytes) < 8:
        key_bytes = key_bytes + b'\x00'*(8-len(key_bytes))
    elif len(key_bytes) > 8:
        key_bytes = key_bytes[:8]
    keybits = bytes_to_bitstr(key_bytes)  # 64-bit
    key56 = permute(keybits, PC1)        # 56-bit
    C = key56[:28]
    D = key56[28:]
    CDs = [(C, D)]  # list C0,D0 ... C16,D16
    subkeys = []
    for r in ROTATIONS:
        C = left_rotate(C, r)
        D = left_rotate(D, r)
        CDs.append((C, D))
        subkey = permute(C + D, PC2)
        subkeys.append(subkey)
    return keybits, CDs, subkeys

# =========================
# Single-block encryption with per-round detailed trace
# =========================

def encrypt_block_trace(block8: bytes, subkeys: list):
    block_bits = bytes_to_bitstr(block8)  # 64-bit string
    trace = {}
    trace['block_bits'] = block_bits
    ip = permute(block_bits, IP)
    trace['IP'] = ip
    L = ip[:32]
    R = ip[32:]
    trace['L0'] = L
    trace['R0'] = R
    rounds = []
    for i in range(16):
        ER = permute(R, E)  # 48-bit
        after_xor = xor_bits(ER, subkeys[i])  # 48-bit
        s_vals, s_combined = sbox_outputs(after_xor)  # list of 8 ints, combined 32b string
        p_out = permute(s_combined, P)  # 32-bit
        newL = R
        newR = xor_bits(L, p_out)
        round_info = {
            'round': i+1,
            'L_before': L,
            'R_before': R,
            'ER': ER,
            'after_xor': after_xor,
            's_vals': s_vals,           # list of ints 0..15
            's_combined': s_combined,   # 32-bit string
            'p_out': p_out,
            'L_after': newL,
            'R_after': newR,
            'K': subkeys[i]
        }
        rounds.append(round_info)
        # update L,R
        L, R = newL, newR
    preoutput = R + L
    cipher_bits = permute(preoutput, IP_INV)
    trace['rounds'] = rounds
    trace['preoutput'] = preoutput
    trace['cipher_bits'] = cipher_bits
    trace['cipher_hex'] = bitstr_to_bytes(cipher_bits).hex().upper()
    return trace

# =========================
# Full DES encryption wrapper (handles padding and multiple blocks)
# =========================

def DES_full_encrypt(plaintext: str, key: str):
    # prepare bytes
    pt_bytes = plaintext.encode('utf-8')
    pt_padded = pkcs7_pad_bytes(pt_bytes)
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 8:
        key_bytes = key_bytes + b'\x00'*(8-len(key_bytes))
    else:
        key_bytes = key_bytes[:8]

    # generate subkeys and CDs
    keybits, CDs, subkeys = generate_subkeys_and_CDs(key_bytes)

    blocks = [pt_padded[i:i+8] for i in range(0, len(pt_padded), 8)]
    block_traces = []
    cipher_blocks = []
    for bl in blocks:
        tr = encrypt_block_trace(bl, subkeys)
        block_traces.append(tr)
        cipher_blocks.append(tr['cipher_bits'])
    full_cipher_bits = ''.join(cipher_blocks)
    full_cipher_hex = bitstr_to_bytes(full_cipher_bits).hex().upper()
    return {
        'keybits': keybits,
        'CDs': CDs,
        'subkeys': subkeys,
        'block_traces': block_traces,
        'full_cipher_bits': full_cipher_bits,
        'full_cipher_hex': full_cipher_hex,
        'padded_plain_hex': pt_padded.hex().upper()
    }

# =========================
# GUI Application
# =========================

class DESApp:
    def __init__(self, root):
        self.root = root
        root.title("DES Explorer — Detailed (Tab per Round)")
        root.geometry("1200x780")

        # style
        style = ttk.Style(root)
        try:
            style.theme_use('clam')
        except:
            pass

        header = tk.Frame(root, bg='#1b2632')
        header.pack(fill='x')
        tk.Label(header, text="DES Explorer — Step-by-step Feistel Rounds (Tab per Round)",
                 bg='#1b2632', fg='#f6f6f6', font=('Helvetica', 14, 'bold'), pady=8).pack()

        # Input frame
        frm = tk.Frame(root, pady=8)
        frm.pack(fill='x')
        tk.Label(frm, text="Plaintext:", width=12, anchor='e').grid(row=0, column=0, padx=6, pady=4)
        self.ent_plain = tk.Entry(frm, width=60)
        self.ent_plain.grid(row=0, column=1, padx=6, pady=4)
        tk.Label(frm, text="Key (max 8 chars):", width=20, anchor='e').grid(row=1, column=0, padx=6, pady=4)
        self.ent_key = tk.Entry(frm, width=30)
        self.ent_key.grid(row=1, column=1, sticky='w', padx=6, pady=4)
        ttk.Button(frm, text="Encrypt & Build Trace", command=self.on_encrypt).grid(row=0, column=2, rowspan=2, padx=8)

        # Notebook: Process Trace | Subkeys | C/D | Ciphertext | Feistel Rounds
        self.nb = ttk.Notebook(root)
        self.nb.pack(fill='both', expand=True, padx=8, pady=8)

        # Tab: Process Trace
        self.tab_trace = ttk.Frame(self.nb)
        self.nb.add(self.tab_trace, text="Process Trace")
        self.txt_trace = scrolledtext.ScrolledText(self.tab_trace, font=('Consolas', 10), bg='#0f1720', fg='#9ae6b4')
        self.txt_trace.pack(fill='both', expand=True, padx=6, pady=6)

        # Tab: Subkeys
        self.tab_subkeys = ttk.Frame(self.nb)
        self.nb.add(self.tab_subkeys, text="Subkeys (K1..K16)")
        self.txt_subkeys = scrolledtext.ScrolledText(self.tab_subkeys, font=('Consolas', 10), bg='#071223', fg='#ffd166')
        self.txt_subkeys.pack(fill='both', expand=True, padx=6, pady=6)

        # Tab: C & D
        self.tab_cd = ttk.Frame(self.nb)
        self.nb.add(self.tab_cd, text="C0..C16 / D0..D16")
        self.txt_cd = scrolledtext.ScrolledText(self.tab_cd, font=('Consolas', 10), bg='#071223', fg='#7ed957')
        self.txt_cd.pack(fill='both', expand=True, padx=6, pady=6)

        # Tab: Ciphertext
        self.tab_cipher = ttk.Frame(self.nb)
        self.nb.add(self.tab_cipher, text="Ciphertext")
        self.txt_cipher = scrolledtext.ScrolledText(self.tab_cipher, font=('Consolas', 11, 'bold'), bg='#071223', fg='#ff6b6b')
        self.txt_cipher.pack(fill='both', expand=True, padx=6, pady=6)

        # Tab: Feistel Rounds (contains nested Notebook with 16 tabs)
        self.tab_feistel = ttk.Frame(self.nb)
        self.nb.add(self.tab_feistel, text="Feistel Rounds (Round Tabs)")
        self.feistel_nb = ttk.Notebook(self.tab_feistel)
        self.feistel_nb.pack(fill='both', expand=True, padx=6, pady=6)

        # create 16 sub-tabs placeholders
        self.round_text_widgets = []
        for i in range(16):
            frame = ttk.Frame(self.feistel_nb)
            self.feistel_nb.add(frame, text=f"Round {i+1}")
            txt = scrolledtext.ScrolledText(frame, font=('Consolas', 10), bg='#071223', fg='#bde0fe')
            txt.pack(fill='both', expand=True, padx=6, pady=6)
            self.round_text_widgets.append(txt)

        # status bar
        self.status = tk.Label(root, text="Ready", bd=1, relief='sunken', anchor='w')
        self.status.pack(fill='x')

        # internal storage
        self.last_result = None

    def on_encrypt(self):
        plaintext = self.ent_plain.get()
        key = self.ent_key.get()
        if plaintext == "":
            messagebox.showwarning("Input missing", "Masukkan plaintext minimal 1 karakter.")
            return
        if key == "":
            messagebox.showwarning("Input missing", "Masukkan key (1–8 karakter).")
            return
        # run DES full
        try:
            res = DES_full_encrypt(plaintext, key)
        except Exception as e:
            messagebox.showerror("Error", f"Proses enkripsi gagal: {e}")
            return
        self.last_result = res
        self.populate_tabs(res)
        self.status.config(text=f"Trace dibuat — Cipher HEX: {res['full_cipher_hex']}")

    def populate_tabs(self, res):
        # Trace tab
        trace_txt = ""
        trace_txt += f"Plaintext (padded hex): {res['padded_plain_hex']}\n"
        trace_txt += f"Key (bits): {res['keybits']}\n\n"
        trace_txt += "=== C0..C16 & D0..D16 ===\n"
        for idx,(c,d) in enumerate(res['CDs']):
            trace_txt += f"C{idx}: {c}\nD{idx}: {d}\n\n"
        trace_txt += "\n=== Subkeys K1..K16 (bin) ===\n"
        for i,k in enumerate(res['subkeys'], start=1):
            trace_txt += f"K{i:02d}: {k}  (hex: {format(int(k,2),'012X')})\n"
        trace_txt += "\n\n=== Per-block rounds (detailed) ===\n\n"
        # only show first block detail in trace (but full cipher gives all blocks)
        for b_idx, btr in enumerate(res['block_traces'], start=1):
            trace_txt += f"--- Block {b_idx} ---\n"
            trace_txt += f"Block bits: {btr['block_bits']}\nIP: {btr['IP']}\nL0: {btr['L0']}\nR0: {btr['R0']}\n\n"
            for r in btr['rounds']:
                trace_txt += f"Round {r['round']}:\n"
                trace_txt += f"  ER: {r['ER']}\n"
                trace_txt += f"  After XOR: {r['after_xor']}\n"
                # S-box individual outputs
                s_list = r['s_vals']
                for si, sval in enumerate(s_list, start=1):
                    trace_txt += f"   S{si}: {format(sval,'04b')} ({sval})\n"
                trace_txt += f"  S combined: {r['s_combined']}\n"
                trace_txt += f"  P: {r['p_out']}\n"
                trace_txt += f"  L(after): {r['L_after']}\n"
                trace_txt += f"  R(after): {r['R_after']}\n\n"
            trace_txt += f"Preoutput: {btr['preoutput']}\nCipher bits: {btr['cipher_bits']}\nCipher HEX (block): {btr['cipher_hex']}\n\n"
        self.txt_trace.delete('1.0', tk.END)
        self.txt_trace.insert(tk.END, trace_txt)

        # Subkeys tab
        self.txt_subkeys.delete('1.0', tk.END)
        for i,k in enumerate(res['subkeys'], start=1):
            self.txt_subkeys.insert(tk.END, f"K{i:02d}: {k}  (hex: {format(int(k,2),'012X')})\n")

        # C & D tab
        self.txt_cd.delete('1.0', tk.END)
        for idx,(c,d) in enumerate(res['CDs']):
            self.txt_cd.insert(tk.END, f"C{idx}: {c}\nD{idx}: {d}\n\n")

        # Cipher tab (full)
        self.txt_cipher.delete('1.0', tk.END)
        self.txt_cipher.insert(tk.END, f"Full ciphertext (bin):\n{res['full_cipher_bits']}\n\n")
        self.txt_cipher.insert(tk.END, f"Full ciphertext (hex):\n{res['full_cipher_hex']}\n")

        # Feistel rounds tabs (per-round tab)
        # Show only first block details per round tab for clarity
        if len(res['block_traces']) == 0:
            return
        block_trace = res['block_traces'][0]
        for i, r in enumerate(block_trace['rounds']):
            txt = self.round_text_widgets[i]
            txt.delete('1.0', tk.END)
            txt.insert(tk.END, f"=== Round {r['round']} ===\n\n")
            txt.insert(tk.END, f"L({r['round']-1}): {r['L_before']}\n")
            txt.insert(tk.END, f"R({r['round']-1}): {r['R_before']}\n\n")
            txt.insert(tk.END, f"E(R):\n{r['ER']}\n\n")
            txt.insert(tk.END, f"XOR with K{r['round']} ({r['K']}):\n{r['after_xor']}\n\n")
            txt.insert(tk.END, "S-Box outputs (each 4-bit):\n")
            for si, sval in enumerate(r['s_vals'], start=1):
                txt.insert(tk.END, f"  S{si}: {format(sval,'04b')}  (decimal {sval})\n")
            txt.insert(tk.END, f"\nS Combined (32b):\n{r['s_combined']}\n\n")
            txt.insert(tk.END, f"P output (32b):\n{r['p_out']}\n\n")
            txt.insert(tk.END, f"L({r['round']}): {r['L_after']}\n")
            txt.insert(tk.END, f"R({r['round']}): {r['R_after']}\n")

# =========================
# Run application
# =========================

def main():
    root = tk.Tk()
    app = DESApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
