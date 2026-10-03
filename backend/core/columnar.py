"""
Columnar Transposition Cipher Engine - Implementasi Murni Tanpa Library Kriptografi
Mata Kuliah: Kriptografi (IF21A05)

Algoritma Transposisi Kolom:
- Menyusun karakter plainteks ke dalam kisi (grid) persegi panjang baris demi baris
- Mengacak urutan pembacaan kolom berdasarkan permutasi alfabetik kata kunci
- Menghasilkan cipherteks dengan membaca kolom per kolom sesuai urutan prioritas kunci
"""

import math
from typing import Dict, Any, List

def get_key_order(key: str) -> List[int]:
    """
    Menentukan urutan kolom berdasarkan urutan alfabet kata kunci (stable sort).
    Contoh: Kunci 'BATU' -> Urutan alfabet: A (1), B (0), T (2), U (3)
    Output ranking untuk tiap posisi: [1, 0, 2, 3]
    """
    clean_k = [ch for ch in key.upper() if ch.isalpha()]
    if not clean_k:
        raise ValueError("Kata kunci Transposisi Kolom wajib mengandung minimal 1 karakter alfabet.")

    # Pasangkan huruf dengan indeks aslinya
    indexed_chars = [(ch, i) for i, ch in enumerate(clean_k)]
    # Urutkan berdasarkan huruf
    sorted_chars = sorted(indexed_chars, key=lambda x: x[0])
    # Urutan indeks kolom yang dibaca
    order = [idx for ch, idx in sorted_chars]
    return order

def columnar_encrypt(plaintext: str, key: str, pad_char: str = 'X') -> Dict[str, Any]:
    """
    Mengenkripsi plainteks menggunakan Transposisi Kolom.
    1. Tentukan jumlah kolom = panjang kata kunci.
    2. Susun plainteks ke dalam grid baris per baris.
    3. Isi sel kosong baris terakhir dengan karakter padding (default 'X').
    4. Baca kolom demi kolom sesuai urutan abjad kata kunci.
    """
    clean_p = [ch for ch in plaintext.upper() if ch.isalpha()]
    clean_k = [ch for ch in key.upper() if ch.isalpha()]
    num_cols = len(clean_k)

    if num_cols == 0:
        raise ValueError("Kata kunci tidak boleh kosong.")

    num_rows = math.ceil(len(clean_p) / num_cols)
    total_cells = num_rows * num_cols

    # Lakukan padding jika diperlukan
    padded_p = clean_p.copy()
    pad_count = total_cells - len(clean_p)
    padded_p.extend([pad_char] * pad_count)

    # Bentuk grid 2D
    grid = []
    for r in range(num_rows):
        row = padded_p[r * num_cols : (r + 1) * num_cols]
        grid.append(row)

    # Ambil urutan pembacaan kolom
    col_order = get_key_order(key)
    ciphertext_cols = []
    ciphertext = []

    for col_idx in col_order:
        col_chars = [grid[r][col_idx] for r in range(num_rows)]
        ciphertext_cols.append({
            "col_index": col_idx,
            "key_char": clean_k[col_idx],
            "chars": "".join(col_chars)
        })
        ciphertext.extend(col_chars)

    return {
        "ciphertext": "".join(ciphertext),
        "clean_plaintext": "".join(clean_p),
        "key": "".join(clean_k),
        "num_rows": num_rows,
        "num_cols": num_cols,
        "grid": grid,
        "col_order": col_order,
        "ciphertext_cols": ciphertext_cols,
        "padded_count": pad_count
    }

def columnar_decrypt(ciphertext: str, key: str, original_length: int = None) -> Dict[str, Any]:
    """
    Mendekripsi cipherteks Transposisi Kolom.
    1. Hitung jumlah baris = len(ciphertext) / num_cols.
    2. Masukkan karakter cipherteks ke dalam kolom sesuai urutan prioritas kunci.
    3. Baca teks hasil dekripsi baris per baris dari kiri ke kanan.
    """
    clean_c = [ch for ch in ciphertext.upper() if ch.isalpha()]
    clean_k = [ch for ch in key.upper() if ch.isalpha()]
    num_cols = len(clean_k)

    if num_cols == 0:
        raise ValueError("Kata kunci tidak boleh kosong.")

    num_rows = math.ceil(len(clean_c) / num_cols)
    col_order = get_key_order(key)

    # Buat grid kosong
    grid = [["" for _ in range(num_cols)] for _ in range(num_rows)]

    # Isi kolom demi kolom sesuai urutan col_order
    char_idx = 0
    for col_idx in col_order:
        for r in range(num_rows):
            if char_idx < len(clean_c):
                grid[r][col_idx] = clean_c[char_idx]
                char_idx += 1

    # Baca baris per baris
    plaintext = []
    for r in range(num_rows):
        plaintext.extend(grid[r])

    res_str = "".join(plaintext)
    if original_length is not None and original_length <= len(res_str):
        res_str = res_str[:original_length]

    return {
        "plaintext": res_str,
        "key": "".join(clean_k),
        "num_rows": num_rows,
        "num_cols": num_cols,
        "grid": grid,
        "col_order": col_order
    }
