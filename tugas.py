# ===============================================
# Tugas Pratikum 2 - Kalkulator Hybrid (Versi Menu)
# ===============================================

def ekspresi_tanpa_spasi():
    print("\n=== Input Ekspresi TANPA spasi ===")
    while True:
        ekspresi = input("Masukkan ekspresi (atau ketik 'kembali' untuk menu): ")
        if ekspresi.lower() == "kembali":
            break
        try:
            hasil = eval(ekspresi)
            print("Hasil Diproses:", ekspresi)
            print("Output (Hasil):", hasil)
            print("--------------------------------------\n")
        except:
            print("Ekspresi tidak valid! Ulangi lagi.\n")

def ekspresi_dengan_spasi():
    print("\n=== Input Ekspresi DENGAN spasi ===")
    while True:
        ekspresi = input("Masukkan ekspresi (atau ketik 'kembali' untuk menu): ")
        if ekspresi.lower() == "kembali":
            break
        try:
            hasil = eval(ekspresi)
            print("Hasil Diproses:", ekspresi)
            print("Output (Hasil):", hasil)
            print("--------------------------------------\n")
        except:
            print("Ekspresi tidak valid! Ulangi lagi.\n")

# ===============================================
# Program Utama (Menu)
# ===============================================
while True:
    print("===============================================")
    print("              KALKULATOR HYBRID                ")
    print("===============================================")
    print("1. Input Ekspresi TANPA spasi")
    print("2. Input Ekspresi DENGAN spasi")
    print("3. Keluar")
    print("===============================================")

    pilih = input("Pilih menu (1-3): ")

    if pilih == "1":
        ekspresi_tanpa_spasi()
    elif pilih == "2":
        ekspresi_dengan_spasi()
    elif pilih == "3":
        print("\nTerima kasih! Program selesai.")
        break
    else:
        print("Pilihan tidak valid! Masukkan angka 1–3.\n")
