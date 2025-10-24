# Konversi Oktal ke Desimal, Biner, dan Hexadesimal

print("=== Konversi Bilangan Oktal ke Desimal, Biner & Hexadesimal ===")
print("Ketik 'keluar' untuk mengakhiri program.\n")

while True:
    oktal = input("Masukkan bilangan oktal: ")

    if oktal.lower() == "keluar":
        print("\nProgram selesai. Terima kasih!")
        break

    try:
        desimal = int(oktal, 8)
        biner = bin(desimal).replace("0b", "")
        heksa = hex(desimal).upper().replace("0X", "")
        print("Hasil Diproses:", oktal)
        print("Output (Desimal)     :", desimal)
        print("Output (Biner)       :", biner)
        print("Output (Hexadesimal) :", heksa)
        print("----------------------------------\n")
    except:
        print("Input tidak valid! Bilangan oktal hanya boleh 0–7.\n")
