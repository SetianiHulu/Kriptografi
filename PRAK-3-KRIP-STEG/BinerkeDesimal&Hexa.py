# Konversi Biner ke Desimal dan Hexadesimal

print("=== Konversi Bilangan Biner ke Desimal & Hexadesimal ===")
print("Ketik 'keluar' untuk mengakhiri program.\n")

while True:
    biner = input("Masukkan bilangan biner: ")

    if biner.lower() == "keluar":
        print("\nProgram selesai. Terima kasih!")
        break

    try:
        desimal = int(biner, 2)
        heksa = hex(desimal).upper().replace("0X", "")
        print("Hasil Diproses:", biner)
        print("Output (Desimal)     :", desimal)
        print("Output (Hexadesimal) :", heksa)
        print("----------------------------------\n")
    except:
        print("Input tidak valid! Pastikan hanya berisi 0 dan 1.\n")
