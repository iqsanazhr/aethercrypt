"""
Super-Encryption Pipeline Engine
Mata Kuliah: Kriptografi (IF21A05)

Menjalankan rantai super-enkripsi 3 tahap:
Tahap 1: Playfair Cipher (Substitusi Poligram)
Tahap 2: Vigenère Cipher (Substitusi Polialfabetik)
Tahap 3: Columnar Transposition (Transposisi Kolom)

Dan rantai dekripsi balik invers:
Tahap 3 Invers: Columnar Transposition Decrypt
Tahap 2 Invers: Vigenère Decrypt
Tahap 1 Invers: Playfair Decrypt
Disertai validasi kebenaran bolak-balik 100% identik.
"""

from typing import Dict, Any
from .playfair import playfair_encrypt, playfair_decrypt
from .vigenere import vigenere_encrypt, vigenere_decrypt
from .columnar import columnar_encrypt, columnar_decrypt

def super_encrypt(
    plaintext: str,
    playfair_key: str,
    vigenere_key: str,
    columnar_key: str
) -> Dict[str, Any]:
    """
    Eksekusi Pipeline Super-Enkripsi 3 Tahap
    P -> [Playfair] -> C1 -> [Vigenère] -> C2 -> [Columnar] -> C_Final
    """
    # Tahap 1: Playfair
    stage1 = playfair_encrypt(plaintext, playfair_key)
    c1 = stage1["ciphertext"]

    # Tahap 2: Vigenère
    stage2 = vigenere_encrypt(c1, vigenere_key)
    c2 = stage2["ciphertext"]

    # Tahap 3: Columnar Transposition
    stage3 = columnar_encrypt(c2, columnar_key)
    c_final = stage3["ciphertext"]

    return {
        "final_ciphertext": c_final,
        "stages": {
            "stage1_playfair": {
                "name": "Playfair Cipher (Substitusi Poligram)",
                "input": "".join(ch for ch in plaintext.upper() if ch.isalpha()),
                "output": c1,
                "matrix": stage1["matrix"],
                "steps": stage1["steps"]
            },
            "stage2_vigenere": {
                "name": "Vigenère Cipher (Substitusi Polialfabetik)",
                "input": c1,
                "output": c2,
                "expanded_key": stage2["expanded_key"],
                "steps": stage2["steps"]
            },
            "stage3_columnar": {
                "name": "Columnar Transposition (Transposisi Kolom)",
                "input": c2,
                "output": c_final,
                "grid": stage3["grid"],
                "col_order": stage3["col_order"],
                "ciphertext_cols": stage3["ciphertext_cols"]
            }
        }
    }

def reconstruct_playfair_text(recovered: str, original_plaintext: str = None) -> str:
    """
    Merekonstruksi plainteks asli dari hasil dekripsi Playfair
    dengan menghilangkan huruf pengisi (filler 'X'/'Z') pada huruf kembar
    serta padding di akhir kalimat secara deterministik.
    """
    if not recovered:
        return ""
    
    # Jika original_plaintext diberikan, rekonstruksi secara deterministik 100%
    if original_plaintext:
        cleaned = [('I' if ch == 'J' else ch) for ch in original_plaintext.upper() if ch.isalpha()]
        insert_indices = set()
        i = 0
        cur_dec_idx = 0
        while i < len(cleaned):
            first = cleaned[i]
            if i + 1 < len(cleaned):
                second = cleaned[i + 1]
                if first == second:
                    # Karakter kedua bigram adalah filler 'X'
                    insert_indices.add(cur_dec_idx + 1)
                    cur_dec_idx += 2
                    i += 1
                else:
                    cur_dec_idx += 2
                    i += 2
            else:
                # Karakter kedua bigram adalah padding akhir
                insert_indices.add(cur_dec_idx + 1)
                cur_dec_idx += 2
                i += 1
                
        reconstructed = [ch for idx, ch in enumerate(recovered) if idx not in insert_indices]
        return "".join(reconstructed)

    # Heuristik mandiri jika original_plaintext tidak tersedia
    chars = list(recovered)
    cleaned = []
    k = 0
    while k < len(chars):
        if k + 2 < len(chars) and chars[k+1] == 'X' and chars[k] == chars[k+2]:
            cleaned.append(chars[k])
            cleaned.append(chars[k+2])
            k += 3
        elif k + 2 < len(chars) and chars[k] == 'X' and chars[k+1] == 'Z' and chars[k+2] == 'X':
            cleaned.append('X')
            cleaned.append('X')
            k += 3
        else:
            cleaned.append(chars[k])
            k += 1
            
    return "".join(cleaned)

def super_decrypt(
    ciphertext: str,
    playfair_key: str,
    vigenere_key: str,
    columnar_key: str,
    original_plaintext: str = None
) -> Dict[str, Any]:
    """
    Eksekusi Pipeline Super-Dekripsi 3 Tahap Invers
    C_Final -> [Inv-Columnar] -> C2 -> [Inv-Vigenère] -> C1 -> [Inv-Playfair] -> P_Final
    """
    # Tahap 3 Invers: Columnar Decrypt
    expected_len = None
    if original_plaintext:
        try:
            expected_len = len(playfair_encrypt(original_plaintext, playfair_key)["ciphertext"])
        except Exception:
            pass

    stage3_inv = columnar_decrypt(ciphertext, columnar_key, original_length=expected_len)
    c2_recovered = stage3_inv["plaintext"]

    # Tahap 2 Invers: Vigenère Decrypt
    stage2_inv = vigenere_decrypt(c2_recovered, vigenere_key)
    c1_recovered = stage2_inv["plaintext"]

    # Tahap 1 Invers: Playfair Decrypt
    stage1_inv = playfair_decrypt(c1_recovered, playfair_key)
    p_raw_recovered = stage1_inv["plaintext"]

    # Validasi kebenaran
    verification = None
    p_final = p_raw_recovered

    if original_plaintext:
        # Normalisasi karakter alfabet (J -> I seperti standar Playfair)
        norm_orig = "".join('I' if ch == 'J' else ch for ch in original_plaintext.upper() if ch.isalpha())
        
        # Rekonstruksi teks dekripsi dengan rekonsiliasi filler 'X' Playfair
        p_reconstructed = reconstruct_playfair_text(p_raw_recovered, norm_orig)
        
        if p_reconstructed == norm_orig:
            is_identical = True
            match_percentage = 100.0
            p_final = p_reconstructed
        else:
            # Hitung kecocokan karakter
            matches = sum(1 for a, b in zip(p_reconstructed, norm_orig) if a == b)
            max_len = max(len(p_reconstructed), len(norm_orig))
            match_percentage = round((matches / max_len) * 100, 2) if max_len > 0 else 100.0
            is_identical = (p_reconstructed == norm_orig)
            p_final = p_reconstructed

        verification = {
            "is_identical": is_identical,
            "match_percentage": match_percentage,
            "original_normalized": norm_orig,
            "decrypted_result": p_final,
            "raw_playfair_decrypted": p_raw_recovered
        }

    return {
        "final_plaintext": p_final,
        "verification": verification,
        "stages": {
            "stage3_inv_columnar": {
                "name": "Inverse Columnar Transposition",
                "output": c2_recovered,
                "grid": stage3_inv["grid"]
            },
            "stage2_inv_vigenere": {
                "name": "Inverse Vigenère Cipher",
                "output": c1_recovered
            },
            "stage1_inv_playfair": {
                "name": "Inverse Playfair Cipher",
                "output": p_raw_recovered
            }
        }
    }
