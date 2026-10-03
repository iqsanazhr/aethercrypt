import sys
import os

from core.pipeline import super_encrypt, super_decrypt
from core.cryptanalysis import analyze_text

plain = "TEMUI SAYA DI LABORATORIUM KRIPTOGRAFI MALAM INI"
k_play = "UNIVERSITAS"
k_vig = "SOEDIRMAN"
k_col = "INFORMATIKA"

print("[*] Input Plaintext:", plain)
enc = super_encrypt(plain, k_play, k_vig, k_col)
c_final = enc["final_ciphertext"]
print("[+] Stage 1 (Playfair):", enc["stages"]["stage1_playfair"]["output"])
print("[+] Stage 2 (Vigenere):", enc["stages"]["stage2_vigenere"]["output"])
print("[+] Stage 3 (Columnar):", enc["stages"]["stage3_columnar"]["output"])
print("[+] Final Ciphertext:", c_final)

dec = super_decrypt(c_final, k_play, k_vig, k_col, original_plaintext=plain)
p_final = dec["final_plaintext"]
print("[+] Decrypted Plaintext:", p_final)
print("[+] Verification:", dec["verification"])

stats_p = analyze_text(plain)
stats_c = analyze_text(c_final)
print(f"[+] IC Plain: {stats_p['ic']} ({stats_p['evaluation']})")
print(f"[+] IC Cipher: {stats_c['ic']} ({stats_c['evaluation']})")
