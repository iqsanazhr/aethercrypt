"""
AetherCrypt - Automated 1,000 Test Sentences Benchmark & Validation Suite
Mata Kuliah: Kriptografi (IF21A05) - Teknik Informatika Unsoed

Script ini menguji kebenaran algoritma super-enkripsi 3 tahap:
Playfair (5x5) -> Vigenère (Modulo 26) -> Columnar Transposition
serta proses dekripsi balik invers:
Columnar Decrypt -> Vigenère Decrypt -> Playfair Decrypt

Menguji 1.000 variasi string pada 5 kategori pengujian:
1. Kalimat Nyata Bahasa Indonesia & Akademik (200 kalimat)
2. Huruf Kembar Ekstrim (Double/Twin Letters: KK, LL, SS, MM, TT, XX, dll) (200 kalimat)
3. Kalimat Berhuruf 'J' Intensif (Normalisasi J -> I) (150 kalimat)
4. Panjang Ganjil & Kasus Batas (Edge Cases, Single Letters, End-of-string X/Z) (150 kalimat)
5. Kalimat Acak Sintetis Berbagai Panjang & Multi-Kunci Dinamis (300 kalimat)
"""

import time
import random
import json
from typing import List, Dict, Any
from core.pipeline import super_encrypt, super_decrypt

# -----------------------------------------------------------------------------
# 1. GENERATOR DATASET PENGUJIAN 1.000 KALIMAT
# -----------------------------------------------------------------------------

def build_test_suite() -> List[Dict[str, Any]]:
    test_cases = []
    
    # -------------------------------------------------------------------------
    # Kategori 1: Kalimat Nyata Bahasa Indonesia & Akademik (200 sampel)
    # -------------------------------------------------------------------------
    real_bases = [
        "SERANGAN SIBER TERDETEKSI PADA JARINGAN SISTEM AKADEMIK KAMPUS TEKNIK",
        "TEMUI SAYA DI LABORATORIUM KRIPTOGRAFI MALAM INI PUKUL DUA PULUH",
        "UNIVERSITAS JENDERAL SOEDIRMAN PURWOKERTO JAWA TENGAH INDONESIA",
        "ALGORITMA SUPER ENKRIPSI MENGGABUNGKAN SUBSTITUSI DAN TRANSPOSISI",
        "LABORATORIUM REKAYASA PERANGKAT LUNAK DAN SISTEM INFORMASI TERPADU",
        "KUNCI RAHASIA HARUS DIJAGA KERAHASIAANNYA AGAR TIDAK BOCOR KE PUBLIK",
        "KRIPTANALISIS MEMBUKTIKAN HISTOGRAM FREKUENSI BERHASIL DIRATAKAN",
        "INDEKS KOINSIDENSI MENDEKATI NILAI ACAK SEMPURNA NOL KOMA NOL TIGA DELAPAN",
        "TRANSPOSISI KOLOM MENGACAK POSISI SPASIAL KARAKTER DENGAN PERMUTASI",
        "PAPAN ROTOR ENIGMA BERPUTAR SECARA PERIODIK SESUAI MODULO DUA PULUH ENAM",
        "MAHASISWA TEKNIK INFORMATIKA MENYELESAIKAN PROYEK AKHIR TEPAT WAKTU",
        "KEAMANAN JARINGAN KAMPUS DILINDUNGI PROTOKOL OTENTIKASI BERLAPIS",
        "INTEGRITAS DATA TERJAMIN DENGAN PENGUJIAN REVERSIBILITAS SERATUS PERSEN",
        "ARSITEKTUR KRIPTOGRAFI KLASIK MENERAPKAN PRINSIP KERCKHOFFS",
        "PENGUJIAN KASISKI TIDAK MAMPU MENEMUKAN PERIODISITAS KUNCI PERIODIK",
        "VALIDASI KEBENARAN MATEMATIKA MENJAMIN PEMULIHAN PESAN TANPA KORUPSI",
        "DATA AKADEMIK MAHASISWA DISIMPAN DALAM SERVER TERSANDI SECARA AMAN",
        "SIMULASI MESIN SANDI MEKANIKAL MENGGUNAKAN VISUALISASI TIGA DIMENSI",
        "DEKRIPSI INVERS BERHASIL MEREKONSTRUKSI PLAINTEXS ASLI DENGAN PRESISI",
        "SANDI DA VINCI CRYPTEX HANYA DAPAT DIBUKA DENGAN KUNCI LIMA HURUF"
    ]
    
    modifiers = [
        "SECARA REAL TIME DAN AKURAT",
        "DENGAN TINGKAT KEAMANAN MAKSIMAL",
        "PADA SERVER PUSAT DATA NASIONAL",
        "UNTUK KEPERLUAN ANALISIS FORENSIK",
        "SESUAI STANDAR KEAMANAN INTERNASIONAL",
        "MENGGUNAKAN ARSITEKTUR TIGA TAHAP",
        "BERDASARKAN PERSAMAAN ALGEBRA MODERN",
        "MELALUI JALUR TRANSMISI ENKRIPSI",
        "DI BAWAH PENGAWASAN TIM KEAMANAN",
        "DENGAN KOMBINASI KATA KUNCI KOMPLEKS"
    ]
    
    cat1_count = 0
    for b in real_bases:
        for m in modifiers:
            if cat1_count >= 200:
                break
            test_cases.append({
                "category": "1. Kalimat Nyata Bahasa Indonesia",
                "text": f"{b} {m}",
                "play_key": "UNSOED",
                "vig_key": "PURWOKERTO",
                "col_key": "INFORMATIKA"
            })
            cat1_count += 1
        if cat1_count >= 200:
            break

    # -------------------------------------------------------------------------
    # Kategori 2: Huruf Kembar Ekstrim (Double / Twin Letters) (200 sampel)
    # Kasus krusial di mana Playfair wajib menyisipkan filler 'X' / 'Z'
    # -------------------------------------------------------------------------
    double_words = [
        "AKADEMIK KAMPUS", "BOOKKEEPER", "SUCCESS", "COMMUNICATION", "COMMITTEE",
        "INTELLIGENCE", "ATTACK", "TRIGGER", "OFFICIAL", "TERDETEKSI KEAMANAN",
        "PASSING MESSAGE", "GOOD DEED", "SWEET TEETH", "POOR ROOSTER", "GREEN NEEDLE",
        "YELLOW WALL", "SMALL BALLOON", "CHEESE WHEEL", "SPEEDY RUNNER", "HIDDEN DOOR",
        "COFFEE BEAN", "CLASSROOM MEETING", "DIFFERENT ADDRESS", "EXCELLENT EFFORT",
        "ILLUMINATION ATTRIBUTE", "SUBMISSION COMPONENT", "PROGRAMMING SKILL"
    ]
    
    for i in range(200):
        # Bangun variasi kalimat dengan banyak huruf kembar
        w1 = double_words[i % len(double_words)]
        w2 = double_words[(i * 3 + 1) % len(double_words)]
        w3 = double_words[(i * 7 + 2) % len(double_words)]
        sentence = f"{w1} PADA {w2} DILENGKAPI {w3} NOMOR {i+100}"
        test_cases.append({
            "category": "2. Huruf Kembar Ekstrim (Playfair Filler)",
            "text": sentence,
            "play_key": "MONARCHY" if i % 2 == 0 else "CRYPTOGRAPHY",
            "vig_key": "SECURITY" if i % 3 == 0 else "MATHEMATICS",
            "col_key": "ALGORITHM" if i % 2 == 0 else "CIPHERTEXT"
        })

    # -------------------------------------------------------------------------
    # Kategori 3: Huruf 'J' Intensif (Normalisasi J -> I) (150 sampel)
    # Memverifikasi bahwa seluruh 'J' dikonversi konsisten menjadi 'I'
    # -------------------------------------------------------------------------
    j_phrases = [
        "JARINGAN JENDERAL JURUSAN JUJUR JANJI JELAJAH JEJAK JUANG",
        "OBJEK PROJEK TAJUK RUJUKAN MAJALAH PENGUJIAN JURNAL ILMIAH",
        "JADWAL PERJALANAN JUANG PRAJURIT MENUJU JALUR PERSIMPANGAN",
        "JAMINAN KEBENARAN JEJAK DIGITAL DALAM RUANG JARINGAN KOMPUTER",
        "KEMAJUAN TEKNOLOGI MENJAMIN KELANJUTAN PROYEK JANGKA PANJANG",
        "JANJI SETIA PRAJURIT JENDERAL SOEDIRMAN MEMPERTAHANKAN JUANG",
        "PENGUJIAN OBJEK TERUJI PADA JARINGAN KOMUNIKASI SISTEM KAMPUS"
    ]
    
    for i in range(150):
        base_j = j_phrases[i % len(j_phrases)]
        sentence = f"{base_j} TAHAP KE {i+1} DIVERIFIKASI SECARA SISTEMATIS"
        test_cases.append({
            "category": "3. Huruf J Intensif (Normalisasi J->I)",
            "text": sentence,
            "play_key": "JENDERAL",
            "vig_key": "JAWATENGAH",
            "col_key": "JURUSAN"
        })

    # -------------------------------------------------------------------------
    # Kategori 4: Panjang Ganjil & Kasus Batas (Edge Cases) (150 sampel)
    # Menguji padding ganjil, kata pendek, dan kata berakhiran X / Z
    # -------------------------------------------------------------------------
    short_words = ["A", "AB", "ABC", "ABCD", "ABCDE", "X", "XX", "XXX", "TEST", "KRIPTO", "CIPHERX", "MATRIX"]
    
    for i in range(150):
        if i < len(short_words):
            text = short_words[i]
        elif i % 3 == 0:
            # String dengan panjang ganjil spesifik
            text = "K" * (2 * (i % 15) + 1)
        elif i % 3 == 1:
            # Berakhiran huruf X atau Z
            text = f"PESAN RAHASIA KEAMANAN BERAKHIRAN HURUF X" if i % 2 == 0 else f"KODE TERSANDI Z"
        else:
            text = f"SAMPEL PENDEK GANJIL NOMOR {i}"
            
        test_cases.append({
            "category": "4. Kasus Batas & Panjang Ganjil",
            "text": text,
            "play_key": "SECRET",
            "vig_key": "KEY",
            "col_key": "BOX"
        })

    # -------------------------------------------------------------------------
    # Kategori 5: Random Generated Stress Strings (300 sampel)
    # Panjang dinamis 15 - 250 karakter, kunci acak, karakter bebas
    # -------------------------------------------------------------------------
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random.seed(42) # Replicable benchmark seed
    
    for i in range(300):
        length = random.randint(15, 220)
        # 80% huruf biasa, 20% spasi
        chars = []
        for _ in range(length):
            if random.random() < 0.15:
                chars.append(" ")
            else:
                chars.append(random.choice(letters))
        rand_text = "".join(chars)
        
        # Kunci acak Playfair, Vigenere, Columnar
        k1 = "".join(random.choices(letters, k=random.randint(5, 10)))
        k2 = "".join(random.choices(letters, k=random.randint(4, 9)))
        k3 = "".join(random.choices(letters, k=random.randint(4, 8)))
        
        test_cases.append({
            "category": "5. Random Generated Stress Strings",
            "text": rand_text,
            "play_key": k1,
            "vig_key": k2,
            "col_key": k3
        })

    return test_cases

# -----------------------------------------------------------------------------
# 2. RUNNER PENGUJIAN OTOMATIS & METRIK BENCHMARK
# -----------------------------------------------------------------------------

def run_stress_test():
    print("=" * 80)
    print("   AETHERCRYPT AUTOMATED VALIDATION SUITE (1,000 TEST SENTENCES)")
    print("   Pipeline: Playfair (5x5) -> Vigenère (Mod 26) -> Columnar Transposition")
    print("=" * 80)
    
    print("\n[*] Menyiapkan 1.000 sampel uji pada 5 kategori...")
    cases = build_test_suite()
    total_cases = len(cases)
    print(f"[+] Total kasus uji berhasil dibentuk: {total_cases} sampel.\n")
    
    passed_count = 0
    failed_count = 0
    failed_samples = []
    
    category_stats = {}
    
    total_chars_processed = 0
    start_all = time.perf_counter()
    
    for idx, tc in enumerate(cases):
        cat = tc["category"]
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "passed": 0, "failed": 0, "time_ms": 0.0}
            
        category_stats[cat]["total"] += 1
        
        raw_text = tc["text"]
        k_play = tc["play_key"]
        k_vig = tc["vig_key"]
        k_col = tc["col_key"]
        
        t0 = time.perf_counter()
        
        # 1. Enkripsi
        enc_res = super_encrypt(raw_text, k_play, k_vig, k_col)
        ciphertext = enc_res["final_ciphertext"]
        
        # 2. Dekripsi
        dec_res = super_decrypt(ciphertext, k_play, k_vig, k_col, original_plaintext=raw_text)
        
        t1 = time.perf_counter()
        elapsed_ms = (t1 - t0) * 1000
        category_stats[cat]["time_ms"] += elapsed_ms
        
        verification = dec_res["verification"]
        is_ok = verification["is_identical"] if verification else False
        
        norm_len = len(verification["original_normalized"]) if verification else len(raw_text)
        total_chars_processed += norm_len
        
        if is_ok:
            passed_count += 1
            category_stats[cat]["passed"] += 1
        else:
            failed_count += 1
            category_stats[cat]["failed"] += 1
            failed_samples.append({
                "index": idx + 1,
                "category": cat,
                "input": raw_text,
                "normalized": verification["original_normalized"] if verification else "",
                "recovered": dec_res["final_plaintext"],
                "match_pct": verification["match_percentage"] if verification else 0
            })
            
        # Progress indicator per 100 cases
        if (idx + 1) % 100 == 0 or idx + 1 == total_cases:
            progress_pct = ((idx + 1) / total_cases) * 100
            print(f"    -> Progress: [{idx + 1:>4}/{total_cases}] ({progress_pct:>5.1f}%) | "
                  f"Lulus: {passed_count:>4} | Gagal: {failed_count:>2}")
            
    total_elapsed = time.perf_counter() - start_all
    avg_latency_ms = (total_elapsed / total_cases) * 1000
    throughput_chars_sec = total_chars_processed / total_elapsed if total_elapsed > 0 else 0
    
    # -------------------------------------------------------------------------
    # 3. LAPORAN STATISTIK EKSEKUTIF
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("                    RINGKASAN BENCHMARK EKSEKUTIF")
    print("=" * 80)
    print(f" Total Kalimat Diuji        : {total_cases:,} Kasus")
    print(f" Status Sukses (100% Match) : {passed_count:,} Kasus ({passed_count/total_cases*100:.2f}%)")
    print(f" Status Gagal (Discrepancy) : {failed_count:,} Kasus ({failed_count/total_cases*100:.2f}%)")
    print(f" Total Karakter Diproses    : {total_chars_processed:,} Karakter")
    print(f" Total Waktu Pengujian      : {total_elapsed:.3f} Detik")
    print(f" Rata-rata Latensi per Uji  : {avg_latency_ms:.3f} ms / kalimat (Enkripsi + Dekripsi)")
    print(f" Throughput Kriptografi     : {throughput_chars_sec:,.0f} karakter / detik")
    print("-" * 80)
    
    print("\nBreakdown Hasil per Kategori Pengujian:")
    print(f"{'Kategori Pengujian':<42} | {'Sampel':<7} | {'Lulus':<7} | {'Persentase':<10} | {'Waktu Rata-rata':<15}")
    print("-" * 90)
    for cat_name, s in category_stats.items():
        pct = (s["passed"] / s["total"]) * 100 if s["total"] > 0 else 0
        avg_t = s["time_ms"] / s["total"] if s["total"] > 0 else 0
        print(f"{cat_name:<42} | {s['total']:<7} | {s['passed']:<7} | {pct:>8.2f}% | {avg_t:>8.3f} ms")
    print("-" * 90)
    
    if failed_count == 0:
        print("\n[OK] SELURUH 1.000 KALIMAT TERBUKTI 100% IDENTIK DAN REVERSIBEL TANPA CACAT DATA!")
        print("     Rumus Kriptografi P -> Enc -> Dec -> P' == P Bekerja Sempurna Secara Matematika.")
    else:
        print(f"\n[!] PERINGATAN: Ditemukan {failed_count} kasus gagal. Contoh kasus gagal pertama:")
        print(json.dumps(failed_samples[:3], indent=2))
        
    print("=" * 80)

if __name__ == "__main__":
    run_stress_test()
