import numpy as np

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None  # Invers matriks/nilai tidak ada
    else:
        return x % m

# 1. CAESAR CIPHER
def caesar(text, mode, key):
    steps = []
    result = ""
    steps.append(f"<b>Rumus Umum:</b> Enkripsi: $C = (P + K) \\pmod{{26}}$, Dekripsi: $P = (C - K) \\pmod{{26}}$")
    steps.append(f"Menggunakan Key (Shift) = {key}")
    
    for i, char in enumerate(text):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p_val = ord(char) - base
            if mode == 'encrypt':
                c_val = (p_val + key) % 26
                res_char = chr(c_val + base)
                steps.append(f"Karakter ke-{i+1} '{char}': $({p_val} + {key}) \\pmod{{26}} = {c_val}$ -> '{res_char}'")
            else:
                c_val = (p_val - key) % 26
                res_char = chr(c_val + base)
                steps.append(f"Karakter ke-{i+1} '{char}': $({p_val} - {key}) \\pmod{{26}} = {c_val}$ -> '{res_char}'")
            result += res_char
        else:
            result += char
            steps.append(f"Karakter ke-{i+1} '{char}': Karakter non-alfabet diabaikan.")
    return result, steps

# 2. VIGENERE CIPHER
def vigenere(text, mode, key_word):
    steps = []
    result = ""
    steps.append("<b>Rumus Umum:</b> $C_i = (P_i + K_i) \\pmod{{26}}$ atau $P_i = (C_i - K_i) \\pmod{{26}}$")
    key_word = key_word.upper()
    
    key_index = 0
    for i, char in enumerate(text):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p_val = ord(char) - base
            k_char = key_word[key_index % len(key_word)]
            k_val = ord(k_char) - ord('A')
            
            if mode == 'encrypt':
                c_val = (p_val + k_val) % 26
                res_char = chr(c_val + base)
                steps.append(f"Karakter ke-{i+1} '{char}' dengan Key '{k_char}' ({k_val}): $({p_val} + {k_val}) \\pmod{{26}} = {c_val}$ -> '{res_char}'")
            else:
                c_val = (p_val - k_val) % 26
                res_char = chr(c_val + base)
                steps.append(f"Karakter ke-{i+1} '{char}' dengan Key '{k_char}' ({k_val}): $({p_val} - {k_val}) \\pmod{{26}} = {c_val}$ -> '{res_char}'")
            
            result += res_char
            key_index += 1
        else:
            result += char
            steps.append(f"Karakter ke-{i+1} '{char}': Karakter non-alfabet diabaikan.")
    return result, steps

# 3. AFFINE CIPHER
def affine(text, mode, a, b):
    steps = []
    result = ""
    steps.append(f"<b>Rumus Umum:</b> Enkripsi: $E(x) = (ax + b) \\pmod{{26}}$. Dekripsi: $D(x) = a^{{-1}}(x - b) \\pmod{{26}}$")
    
    a_inv = modinv(a, 26)
    if mode == 'decrypt' and a_inv is None:
        return "ERROR", [f"Nilai a={a} tidak koprima dengan 26. Dekripsi mustahil dilakukan!"]
        
    steps.append(f"Parameter: a = {a}, b = {b}. Invers modular dari a mod 26 = {a_inv}")
    
    for i, char in enumerate(text):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            if mode == 'encrypt':
                res_val = (a * x + b) % 26
                res_char = chr(res_val + base)
                steps.append(f"Karakter ke-{i+1} '{char}' ($x={x}$): $({a} \\times {x} + {b}) \\pmod{{26}} = {res_val}$ -> '{res_char}'")
            else:
                res_val = (a_inv * (x - b)) % 26
                res_char = chr(res_val + base)
                steps.append(f"Karakter ke-{i+1} '{char}' ($x={x}$): ${a_inv} \\times ({x} - {b}) \\pmod{{26}} = {res_val}$ -> '{res_char}'")
            result += res_char
        else:
            result += char
    return result, steps

# 4. HILL CIPHER
def hill(text, mode, matrix_flat, size):
    steps = []
    # Bersihkan teks hanya alfabet (Hill Cipher membutuhkan blok berukuran pas)
    clean_text = "".join([c.upper() for c in text if c.isalpha()])
    steps.append(f"Pembersihan Teks: Mengubah ke uppercase dan membuang karakter non-alfabet -> {clean_text}")
    
    try:
        K = np.array(matrix_flat).reshape(size, size) % 26
    except:
        return "ERROR", ["Ukuran matriks kunci tidak sesuai."]
    
    steps.append(f"Matriks Kunci K:<br><pre>{K}</pre>")
    
    # Padding jika panjang tidak mencukupi ukuran blok
    while len(clean_text) % size != 0:
        clean_text += 'X'
        steps.append("Padding ditambahkan: 'X'")
        
    if mode == 'encrypt':
        result = ""
        steps.append("<b>Proses Perkalian Matriks Enkripsi ($C = K \\times P \\pmod{{26}}$):</b>")
        for i in range(0, len(clean_text), size):
            block = clean_text[i:i+size]
            p_vector = np.array([ord(c) - ord('A') for c in block])
            c_vector = np.dot(K, p_vector) % 26
            res_block = "".join([chr(int(v) + ord('A')) for v in c_vector])
            steps.append(f"Blok '{block}' {p_vector.tolist()} $\\rightarrow K \\times {p_vector.tolist()} \\pmod{{26}} = {c_vector.tolist()}$ $\\rightarrow$ '{res_block}'")
            result += res_block
        return result, steps
    else:
        # Dekripsi memerlukan invers matriks K mod 26
        det = int(round(np.linalg.det(K))) % 26
        det_inv = modinv(det, 26)
        if det_inv is None:
            return "ERROR", [f"Determinan matriks ({det}) tidak memiliki invers modular 26. Matriks tidak valid untuk dekripsi!"]
        
        # Cari matriks adjugate untuk ukuran 2x2 atau 3x3
        if size == 2:
            adj = np.array([[K[1,1], -K[0,1]], [-K[1,0], K[0,0]]])
        else: # 3x3 manual cofactor matrix shortcut / approach
            adj = np.zeros((3,3))
            for r in range(3):
                for c in range(3):
                    sub = np.delete(np.delete(K, r, axis=0), c, axis=1)
                    adj[c, r] = ((-1)**(r+c) * int(round(np.linalg.det(sub)))) % 26
                    
        K_inv = (det_inv * adj).astype(int) % 26
        steps.append(f"Determinan K = {det}, Invers Determinan = {det_inv}")
        steps.append(f"Matriks Invers K^-1 mod 26:<br><pre>{K_inv}</pre>")
        
        result = ""
        steps.append("<b>Proses Perkalian Matriks Dekripsi ($P = K^{{-1}} \\times C \\pmod{{26}}$):</b>")
        for i in range(0, len(clean_text), size):
            block = clean_text[i:i+size]
            c_vector = np.array([ord(c) - ord('A') for c in block])
            p_vector = np.dot(K_inv, c_vector) % 26
            res_block = "".join([chr(int(v) + ord('A')) for v in p_vector])
            steps.append(f"Blok '{block}' {c_vector.tolist()} $\\rightarrow K^{{-1}} \\times {c_vector.tolist()} \\pmod{{26}} = {p_vector.tolist()}$ $\\rightarrow$ '{res_block}'")
            result += res_block
        return result, steps

# 5. PLAYFAIR CIPHER
def generate_playfair_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    seen = set()
    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair(text, mode, key_word):
    steps = []
    matrix = generate_playfair_matrix(key_word)
    
    # Tampilkan matriks ke dalam visualisasi langkah
    matrix_str = "<table class='table table-bordered text-center w-50 mx-auto'>"
    for row in matrix:
        matrix_str += "<tr>" + "".join([f"<td><b>{cell}</b></td>" for cell in row]) + "</tr>"
    matrix_str += "</table>"
    steps.append(f"Matriks Playfair 5x5 yang digenerate:<br>{matrix_str}")
    
    # Cari posisi karakter
    def find_pos(char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    # Bersihkan teks (Ganti J dengan I)
    clean_text = "".join([c.upper().replace('J', 'I') for c in text if c.isalpha()])
    
    # Proses Pairing (Digraph)
    pairs = []
    i = 0
    while i < len(clean_text):
        a = clean_text[i]
        if i + 1 < len(clean_text):
            b = clean_text[i+1]
            if a == b:
                pairs.append(a + 'X')
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + 'X')
            i += 1
            
    steps.append(f"Hasil pembuatan pasangan huruf (Digraph): {', '.join(pairs)}")
    
    result = []
    for pair in pairs:
        r1, c1 = find_pos(pair[0])
        r2, c2 = find_pos(pair[1])
        
        if r1 == r2: # Baris sama
            shift = 1 if mode == 'encrypt' else -1
            n1 = matrix[r1][(c1 + shift) % 5]
            n2 = matrix[r2][(c2 + shift) % 5]
            steps.append(f"Pasangan '{pair}': Berada di baris yang sama. Digeser menjadi '{n1}{n2}'")
        elif c1 == c2: # Kolom sama
            shift = 1 if mode == 'encrypt' else -1
            n1 = matrix[(r1 + shift) % 5][c1]
            n2 = matrix[(r2 + shift) % 5][c2]
            steps.append(f"Pasangan '{pair}': Berada di kolom yang sama. Digeser menjadi '{n1}{n2}'")
        else: # Membentuk persegi (Box)
            n1 = matrix[r1][c2]
            n2 = matrix[r2][c1]
            steps.append(f"Pasangan '{pair}': Membentuk persegi sudut. Diambil sudut berlawanan menjadi '{n1}{n2}'")
        result.append(n1 + n2)
        
    return "".join(result), steps