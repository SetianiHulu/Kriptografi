import operator

# Dictionary untuk menyimpan operator aritmatika
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# Program utama dengan perulangan
while True:
    pilihan = input("Apakah Anda ingin memulai operasi perhitungan? (Y/T): ").lower()
    
    if pilihan != 'y':
        print("Program selesai. Terima kasih!")
        break  # keluar dari perulangan

    # Input nilai a dan b
    a = float(input("Masukkan nilai a: "))
    b = float(input("Masukkan nilai b: "))

    # Input operator
    c = input("Masukkan operator (+, -, *, /): ")

    # Proses perhitungan dengan penanganan error
    try:
        hasil = ops[c](a, b)
        print(f"Hasil dari {a} {c} {b} = {hasil}")
    except KeyError:
        print("❌ Operator tidak valid. Gunakan +, -, *, atau /")
    except ZeroDivisionError:
        print("❌ Pembagian dengan nol tidak diperbolehkan.")

    print("-" * 40)
