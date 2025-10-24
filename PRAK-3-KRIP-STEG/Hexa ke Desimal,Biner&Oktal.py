# Konversi Hexadesimal ke Desimal, Biner, dan Oktal

print("=== Konversi Bilangan Hexadesimal ke Desimal, Biner & Oktal ===")
print("Ketik 'keluar' untuk mengakhiri program.\n")

while True:
    heksa = input("Masukkan bilangan hexadesimal: ")

    if heksa.lower() == "keluar":
        print("\nProgram selesai. Terima kasih!")
        break

    try:
        desimal = int(heksa, 16)
        biner = bin(desimal).replace("0b", "")
        oktal = oct(desimal).replace("0o", "")
        print("Hasil Diproses:", heksa)
        print("Output (Desimal) :", desimal)
        print("Output (Biner)   :", biner)
        print("Output (Oktal)   :", oktal)
        print("----------------------------------\n")
    except:
        print("Input tidak valid! Gunakan angka 0–9 atau huruf A–F.\n")
