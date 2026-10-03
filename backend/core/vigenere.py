"""
Vigenère Cipher Engine - Implementasi Murni Tanpa Library Kriptografi
Mata Kuliah: Kriptografi (IF21A05)

Algoritma Substitusi Polialfabetik:
- Pergeseran abjad-majemuk menggunakan kata kunci periodik
- Persamaan Enkripsi: C_i = (P_i + K_i) mod 26
- Persamaan Dekripsi: P_i = (C_i - K_i + 26) mod 26
- Visualisasi Bujursangkar Vigenère (Vigenère Tableau 26x26)
"""

from typing import Dict, Any, List

def get_vigenere_tableau() -> List[List[str]]:
    """Menghasilkan matriks bujursangkar Vigenère 26x26"""
    tableau = []
    for r in range(26):
        row = [chr(65 + ((r + c) % 26)) for c in range(26)]
        tableau.append(row)
    return tableau

def vigenere_encrypt(plaintext: str, key: str) -> Dict[str, Any]:
    """
    Mengenkripsi teks menggunakan Vigenère Cipher.
    1. Bersihkan plainteks dan kunci menjadi huruf kapital A-Z.
    2. Perpanjang kunci secara periodik agar sesuai dengan panjang plainteks.
    3. Untuk setiap karakter i: C_i = (P_i + K_i) mod 26
    """
    clean_p = [ch for ch in plaintext.upper() if ch.isalpha()]
    clean_k = [ch for ch in key.upper() if ch.isalpha()]

    if not clean_k:
        raise ValueError("Kata kunci Vigenère wajib mengandung minimal 1 karakter alfabet.")

    ciphertext = []
    steps = []

    for i, p_char in enumerate(clean_p):
        k_char = clean_k[i % len(clean_k)]
        p_val = ord(p_char) - 65
        k_val = ord(k_char) - 65
        c_val = (p_val + k_val) % 26
        c_char = chr(c_val + 65)

        ciphertext.append(c_char)
        steps.append({
            "index": i,
            "p_char": p_char,
            "p_val": p_val,
            "k_char": k_char,
            "k_val": k_val,
            "c_char": c_char,
            "c_val": c_val,
            "formula": f"({p_val} + {k_val}) mod 26 = {c_val} ({c_char})"
        })

    return {
        "ciphertext": "".join(ciphertext),
        "clean_plaintext": "".join(clean_p),
        "expanded_key": "".join(clean_k[i % len(clean_k)] for i in range(len(clean_p))),
        "steps": steps
    }

def vigenere_decrypt(ciphertext: str, key: str) -> Dict[str, Any]:
    """
    Mendekripsi teks menggunakan Vigenère Cipher.
    Persamaan Dekripsi: P_i = (C_i - K_i + 26) mod 26
    """
    clean_c = [ch for ch in ciphertext.upper() if ch.isalpha()]
    clean_k = [ch for ch in key.upper() if ch.isalpha()]

    if not clean_k:
        raise ValueError("Kata kunci Vigenère wajib mengandung minimal 1 karakter alfabet.")

    plaintext = []
    steps = []

    for i, c_char in enumerate(clean_c):
        k_char = clean_k[i % len(clean_k)]
        c_val = ord(c_char) - 65
        k_val = ord(k_char) - 65
        p_val = (c_val - k_val + 26) % 26
        p_char = chr(p_val + 65)

        plaintext.append(p_char)
        steps.append({
            "index": i,
            "c_char": c_char,
            "c_val": c_val,
            "k_char": k_char,
            "k_val": k_val,
            "p_char": p_char,
            "p_val": p_val,
            "formula": f"({c_val} - {k_val} + 26) mod 26 = {p_val} ({p_char})"
        })

    return {
        "plaintext": "".join(plaintext),
        "clean_ciphertext": "".join(clean_c),
        "expanded_key": "".join(clean_k[i % len(clean_k)] for i in range(len(clean_c))),
        "steps": steps
    }
