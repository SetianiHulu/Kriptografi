# Program untuk memahami konsep if dengan kombinasi logika dan aritmatika

# Input nilai dari keyboard
x = int(input("Masukkan nilai x: "))
y = int(input("Masukkan nilai y: "))
z = int(input("Masukkan nilai z: "))

print("\n=== HASIL ANALISIS ===")

# 1. Mengecek apakah x berada di antara 18 dan 30
if x >= 18 and x <= 30:
    print("x berada di antara 18 dan 30")
else:
    print("x tidak berada di antara 18 dan 30")

# 2. Mengecek apakah y berada di luar rentang 10 - 20
if y < 10 or y > 20:
    print("y berada di luar rentang 10 hingga 20")
else:
    print("y berada di dalam rentang 10 hingga 20")

# 3. Mengecek apakah z sama dengan 5
if z == 5:
    print("z sama dengan 5")
else:
    print("z tidak sama dengan 5")

# 4. Mengecek apakah x tidak sama dengan y
if x != y:
    print("x tidak sama dengan y")
else:
    print("x sama dengan y")

# 5. Mengecek apakah x lebih besar dari y
if x > y:
    print("x lebih besar dari y")
else:
    print("x tidak lebih besar dari y")

# 6. Mengecek apakah z lebih kecil dari y
if z < y:
    print("z lebih kecil dari y")
else:
    print("z tidak lebih kecil dari y")

# 7. Kombinasi logika 'and' untuk dua kondisi sekaligus
if y >= 15 and z <= 5:
    print("y lebih besar atau sama dengan 15, dan z lebih kecil atau sama dengan 5")
else:
    print("Salah satu atau kedua kondisi tidak terpenuhi")

print("\n=== Program Selesai ===")
