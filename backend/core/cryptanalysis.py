"""
Cryptanalysis Laboratory Engine - Forensik Frekuensi & Index of Coincidence
Mata Kuliah: Kriptografi (IF21A05)

Modul analisis kripto:
1. Menghitung distribusi frekuensi kemunculan 26 alfabet Latin (A-Z)
2. Menghitung Index of Coincidence (IC) untuk mengukur tingkat keacakan teks
3. Menghitung Entropi Shannon (derajat ketidakpastian informasi)
4. Membandingkan dengan profil statistik bahasa Indonesia dan bahasa Inggris
"""

import math
from collections import Counter
from typing import Dict, Any

# Frekuensi huruf standar bahasa Indonesia (%)
FREQ_INDONESIA = {
    'A': 19.33, 'B': 2.37, 'C': 0.72, 'D': 4.14, 'E': 8.67, 'F': 0.28,
    'G': 3.74,  'H': 2.22, 'I': 8.16, 'J': 0.78, 'K': 5.25, 'L': 3.34,
    'M': 4.11,  'N': 8.62, 'O': 1.63, 'P': 2.74, 'Q': 0.01, 'R': 5.43,
    'S': 4.13,  'T': 5.17, 'U': 5.22, 'V': 0.17, 'W': 0.47, 'X': 0.03,
    'Y': 1.54,  'Z': 0.04
}

# Frekuensi huruf standar bahasa Inggris (%)
FREQ_ENGLISH = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70, 'F': 2.23,
    'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15, 'K': 0.77,  'L': 4.03,
    'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93, 'Q': 0.10,  'R': 5.99,
    'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36,  'X': 0.15,
    'Y': 1.97, 'Z': 0.07
}

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Melakukan analisis kriptanalisis lengkap terhadap suatu teks:
    - Frekuensi absolut dan persentase setiap huruf A-Z
    - Index of Coincidence (IC)
    - Shannon Entropy
    """
    clean_chars = [ch for ch in text.upper() if ch.isalpha()]
    total_len = len(clean_chars)

    if total_len == 0:
        return {
            "total_chars": 0,
            "ic": 0.0,
            "entropy": 0.0,
            "frequencies": [],
            "evaluation": "Teks kosong atau tidak mengandung karakter alfabet."
        }

    counts = Counter(clean_chars)
    frequencies = []

    # Hitung frekuensi tiap huruf A-Z
    sum_fi_fi_minus_1 = 0
    entropy = 0.0

    for code in range(65, 91):
        letter = chr(code)
        count = counts.get(letter, 0)
        percentage = round((count / total_len) * 100, 2)
        p = count / total_len if total_len > 0 else 0

        if count > 0:
            sum_fi_fi_minus_1 += count * (count - 1)
            entropy -= p * math.log2(p)

        frequencies.append({
            "letter": letter,
            "count": count,
            "percentage": percentage,
            "ref_indonesia": FREQ_INDONESIA.get(letter, 0),
            "ref_english": FREQ_ENGLISH.get(letter, 0)
        })

    # Formula Index of Coincidence: IC = sum(f_i * (f_i - 1)) / (N * (N - 1))
    if total_len > 1:
        ic = sum_fi_fi_minus_1 / (total_len * (total_len - 1))
    else:
        ic = 0.0

    # Evaluasi kriptanalisis
    if ic >= 0.060:
        eval_text = "Tinggi (Khas Teks Alami / Substitusi Monoalfabetik sederhana. Rentan terhadap analisis frekuensi)."
    elif ic >= 0.045:
        eval_text = "Sedang (Substitusi Polialfabetik periode pendek)."
    else:
        eval_text = "Rendah mendekati keacakan murni (~0.0385). Berhasil meratakan histogram frekuensi (Tahan kriptanalisis statistik)."

    return {
        "total_chars": total_len,
        "ic": round(ic, 5),
        "entropy": round(entropy, 3),
        "frequencies": frequencies,
        "evaluation": eval_text
    }
