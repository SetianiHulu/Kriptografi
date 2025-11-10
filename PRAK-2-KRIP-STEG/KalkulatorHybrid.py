# === Program Kalkulator Hybrid ===
print("=== Selamat Datang di Program Kalkulator Hybrid ===")

while True:
    print("\nPilih menu:")
    print("1. Hitung ekspresi matematika (misal: 4+4-3 atau 5 - 3 * 4)")
    print("2. Keluar")

    pilihan = input("Masukkan pilihan (1/2): ")

    if pilihan == '1':
        # Input ekspresi
        ekspresi = input("\nMasukkan ekspresi matematika: ")

        try:
            # Hapus spasi
            ekspresi_bersih = ekspresi.replace(" ", "")
            # Hitung hasil ekspresi
            hasil = eval(ekspresi_bersih)
            print("Output >", hasil)
        except Exception as e:
            print("Terjadi kesalahan dalam perhitungan!")
            print("Pesan error:", e)

        # Tanya apakah ingin menghitung ulang
        ulang = input("\nApakah ingin menghitung lagi? (y/t): ").lower()
        if ulang != 'y':
            print("Terima kasih telah menggunakan Kalkulator Hybrid!")
            break

    elif pilihan == '2':
        print("Program selesai. Terima kasih!")
        break

    else:
        print("Pilihan tidak valid! Silakan pilih 1 atau 2.")
