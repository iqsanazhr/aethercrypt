"""
Playfair Cipher Engine - Implementasi Murni Tanpa Library Kriptografi
Mata Kuliah: Kriptografi (IF21A05)

Algoritma Substitusi Poligram:
- Memproses pasangan huruf (bigram)
- Menggunakan matriks bujursangkar 5x5
- Menghilangkan huruf 'J' (digabung dengan 'I')
"""

from typing import List, Tuple, Dict, Any

def create_playfair_matrix(key: str) -> List[List[str]]:
    """
    Menyusun matriks bujursangkar 5x5 berdasarkan kata kunci.
    1. Bersihkan karakter non-alfabet dan ubah ke kapital.
    2. Ganti huruf 'J' dengan 'I'.
    3. Hilangkan huruf duplikat dalam kunci dengan mempertahankan kemunculan pertama.
    4. Isi sisa sel matriks dengan huruf alfabet Latin A-Z (tanpa J) yang belum terpakai.
    """
    clean_key = ""
    for ch in key.upper():
        if ch.isalpha():
            ch = 'I' if ch == 'J' else ch
            if ch not in clean_key:
                clean_key += ch

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # 25 huruf (tanpa J)
    for ch in alphabet:
        if ch not in clean_key:
            clean_key += ch

    # Bentuk matriks 5x5
    matrix = []
    for r in range(5):
        row = list(clean_key[r * 5 : (r + 1) * 5])
        matrix.append(row)
    return matrix

def find_position(matrix: List[List[str]], char: str) -> Tuple[int, int]:
    """Mencari posisi koordinat (baris, kolom) dari suatu karakter dalam matriks 5x5"""
    char = 'I' if char == 'J' else char
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    raise ValueError(f"Karakter '{char}' tidak ditemukan dalam matriks Playfair.")

def prepare_playfair_text(text: str) -> List[str]:
    """
    Menyiapkan plainteks ke dalam kumpulan pasangan huruf (bigram):
    1. Hanya ambil karakter huruf alfabet kapital, 'J' diganti 'I'.
    2. Jika terdapat huruf ganda berturut-turut pada bigram yang sama, sisipkan huruf 'X'.
    3. Jika panjang teks ganjil, tambahkan huruf 'X' di akhir (atau 'Z' jika huruf terakhir X).
    """
    cleaned = []
    for ch in text.upper():
        if ch.isalpha():
            cleaned.append('I' if ch == 'J' else ch)

    bigrams = []
    i = 0
    while i < len(cleaned):
        first = cleaned[i]
        if i + 1 < len(cleaned):
            second = cleaned[i + 1]
            if first == second:
                # Huruf kembar di dalam satu bigram -> sisipkan 'X'
                bigrams.append(first + 'X')
                i += 1
            else:
                bigrams.append(first + second)
                i += 2
        else:
            # Karakter terakhir sendirian (panjang ganjil) -> padding 'X'
            padding = 'Z' if first == 'X' else 'X'
            bigrams.append(first + padding)
            i += 1
    return bigrams

def playfair_encrypt(plaintext: str, key: str) -> Dict[str, Any]:
    """
    Mengenkripsi plainteks menggunakan Playfair Cipher.
    Aturan Enkripsi Bigram:
    1. Baris Sama: Tiap huruf diganti dengan huruf di sebelah kanannya (siklik mod 5).
    2. Kolom Sama: Tiap huruf diganti dengan huruf di bawahnya (siklik mod 5).
    3. Sudut Persegi Panjang: Tiap huruf diganti dengan huruf pada baris yang sama namun kolom huruf pasangannya.
    """
    matrix = create_playfair_matrix(key)
    bigrams = prepare_playfair_text(plaintext)
    cipher_bigrams = []
    steps = []

    for bg in bigrams:
        c1, c2 = bg[0], bg[1]
        r1, col1 = find_position(matrix, c1)
        r2, col2 = find_position(matrix, c2)

        if r1 == r2:
            # Aturan 1: Baris Sama -> Geser ke kanan (siklik)
            new_col1 = (col1 + 1) % 5
            new_col2 = (col2 + 1) % 5
            enc1 = matrix[r1][new_col1]
            enc2 = matrix[r2][new_col2]
            rule = "SAME_ROW"
            desc = f"Sebaris (baris {r1}): geser ke kanan -> {enc1}{enc2}"
        elif col1 == col2:
            # Aturan 2: Kolom Sama -> Geser ke bawah (siklik)
            new_r1 = (r1 + 1) % 5
            new_r2 = (r2 + 1) % 5
            enc1 = matrix[new_r1][col1]
            enc2 = matrix[new_r2][col2]
            rule = "SAME_COLUMN"
            desc = f"Sekolom (kolom {col1}): geser ke bawah -> {enc1}{enc2}"
        else:
            # Aturan 3: Persegi Panjang -> Tukar kolom
            enc1 = matrix[r1][col2]
            enc2 = matrix[r2][col1]
            rule = "RECTANGLE"
            desc = f"Persegi ({r1},{col1}) & ({r2},{col2}) -> sudut seberang: {enc1}{enc2}"

        cipher_bigrams.append(enc1 + enc2)
        steps.append({
            "in": bg,
            "out": enc1 + enc2,
            "rule": rule,
            "pos_in": [[r1, col1], [r2, col2]],
            "pos_out": [[r1 if r1 == r2 else (new_r1 if col1 == col2 else r1), 
                         col2 if r1 != r2 and col1 != col2 else (new_col1 if r1 == r2 else col1)],
                        [r2 if r1 == r2 else (new_r2 if col1 == col2 else r2), 
                         col1 if r1 != r2 and col1 != col2 else (new_col2 if r1 == r2 else col2)]],
            "description": desc
        })

    ciphertext = "".join(cipher_bigrams)
    return {
        "ciphertext": ciphertext,
        "matrix": matrix,
        "input_bigrams": bigrams,
        "cipher_bigrams": cipher_bigrams,
        "steps": steps
    }

def playfair_decrypt(ciphertext: str, key: str) -> Dict[str, Any]:
    """
    Mendekripsi cipherteks Playfair (kebalikan dari enkripsi).
    Aturan Dekripsi:
    1. Baris Sama: Geser ke kiri (siklik mod 5).
    2. Kolom Sama: Geser ke atas (siklik mod 5).
    3. Persegi Panjang: Tukar kolom.
    """
    matrix = create_playfair_matrix(key)
    # Bersihkan ciphertext hanya huruf
    cleaned = [ch for ch in ciphertext.upper() if ch.isalpha()]
    bigrams = [cleaned[i] + cleaned[i+1] for i in range(0, len(cleaned) - 1, 2)]
    plain_bigrams = []
    steps = []

    for bg in bigrams:
        c1, c2 = bg[0], bg[1]
        r1, col1 = find_position(matrix, c1)
        r2, col2 = find_position(matrix, c2)

        if r1 == r2:
            new_col1 = (col1 - 1 + 5) % 5
            new_col2 = (col2 - 1 + 5) % 5
            dec1 = matrix[r1][new_col1]
            dec2 = matrix[r2][new_col2]
            rule = "SAME_ROW"
        elif col1 == col2:
            new_r1 = (r1 - 1 + 5) % 5
            new_r2 = (r2 - 1 + 5) % 5
            dec1 = matrix[new_r1][col1]
            dec2 = matrix[new_r2][col2]
            rule = "SAME_COLUMN"
        else:
            dec1 = matrix[r1][col2]
            dec2 = matrix[r2][col1]
            rule = "RECTANGLE"

        plain_bigrams.append(dec1 + dec2)
        steps.append({
            "in": bg,
            "out": dec1 + dec2,
            "rule": rule
        })

    plaintext = "".join(plain_bigrams)
    return {
        "plaintext": plaintext,
        "matrix": matrix,
        "cipher_bigrams": bigrams,
        "plain_bigrams": plain_bigrams,
        "steps": steps
    }
