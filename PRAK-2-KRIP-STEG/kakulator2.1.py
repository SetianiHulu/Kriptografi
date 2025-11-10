# Kalkulator Sederhana Menggunakan Python

def tambah(a, b):
    return a + b

def kurang(a, b):
    return a - b

def kali(a, b):
    return a * b

def bagi(a, b):
    if b != 0:
        return a / b
    else:
        return "Error! Tidak bisa dibagi dengan nol."

# Program utama dengan perulangan
while True:
    print("\n=== KALKULATOR SEDERHANA ===")
    print("1. Tambah (+)")
    print("2. Kurang (-)")
    print("3. Kali (*)")
    print("4. Bagi (/)")
    print("=============================")

    # Input pilihan operasi
    pilihan = input("Pilih operasi (1/2/3/4): ")

    # Input nilai a dan b
    a = float(input("Masukkan nilai a: "))
    b = float(input("Masukkan nilai b: "))

    # Proses perhitungan
    if pilihan == '1':
        print(f"Hasil: {a} + {b} = {tambah(a, b)}")
    elif pilihan == '2':
        print(f"Hasil: {a} - {b} = {kurang(a, b)}")
    elif pilihan == '3':
        print(f"Hasil: {a} × {b} = {kali(a, b)}")
    elif pilihan == '4':
        print(f"Hasil: {a} ÷ {b} = {bagi(a, b)}")
    else:
        print("❌ Pilihan tidak valid.")

    # Tanya apakah ingin menghitung lagi
    ulang = input("\nApakah ingin menghitung lagi? (Y/T): ").lower()
    if ulang != 'y':
        print("Terima kasih telah menggunakan kalkulator sederhana!")
        break
