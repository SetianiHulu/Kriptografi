# Tugas Pratikum 2: Kalkulator Hybrid (Versi Bisa Diulang)

print("=== Kalkulator Hybrid ===")
print("Masukkan ekspresi matematika (contoh: 4+4-3 atau 5 - 3 * 4)")
print("Ketik 'keluar' untuk mengakhiri program")
print("=====================================\n")

while True:
    # Input Ekspresi
    ekspresi = input("Input (Ekspresi): ")

    # Jika pengguna ingin keluar
    if ekspresi.lower() == "keluar":
        print("\nProgram selesai. Terima kasih!")
        break

    # Proses dan Output
    try:
        hasil = eval(ekspresi)
        print("Hasil Diproses:", ekspresi)
        print("Output (Hasil):", hasil)
        print("------------------------------------\n")
    except:
        print("Terjadi kesalahan dalam memproses ekspresi!\n")
