# Program Kalkulator Sederhana
print("=== Program Kalkulator Sederhana ===")

# Input nilai a dan b
a = float(input("Masukkan nilai a: "))
b = float(input("Masukkan nilai b: "))

# Input operator
operator = input("Masukkan operator (+, -, *, /, %): ")

# Proses perhitungan menggunakan if
if operator == '+':
    hasil = a + b
    print("Hasil:", hasil)
elif operator == '-':
    hasil = a - b
    print("Hasil:", hasil)
elif operator == '*':
    hasil = a * b
    print("Hasil:", hasil)
elif operator == '/':
    if b != 0:
        hasil = a / b
        print("Hasil:", hasil)
    else:
        print("Error: Tidak bisa dibagi dengan nol!")
elif operator == '%':
    hasil = a % b
    print("Hasil:", hasil)
else:
    print("Operator tidak dikenal!")

print("=== Program Selesai ===")
