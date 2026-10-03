"""
AetherCrypt Backend API Server
FastAPI Server untuk Laboratorium Kriptografi Klasik & Super-Enkripsi 3 Tahap
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from core.playfair import playfair_encrypt, playfair_decrypt, create_playfair_matrix
from core.vigenere import vigenere_encrypt, vigenere_decrypt, get_vigenere_tableau
from core.columnar import columnar_encrypt, columnar_decrypt
from core.pipeline import super_encrypt, super_decrypt
from core.cryptanalysis import analyze_text

app = FastAPI(
    title="AetherCrypt Classical Cryptosystem API",
    description="Backend API untuk Super-Enkripsi 3 Tahap (Playfair + Vigenère + Columnar) & Kriptanalisis Forensik",
    version="1.0.0"
)

# Aktifkan CORS untuk React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Schema Data Request ===

class PipelineEncryptRequest(BaseModel):
    plaintext: str = Field(..., description="Plainteks yang akan dienkripsi")
    playfair_key: str = Field("SECRET", description="Kata kunci untuk Playfair Cipher")
    vigenere_key: str = Field("CRYPTO", description="Kata kunci untuk Vigenère Cipher")
    columnar_key: str = Field("CIPHER", description="Kata kunci untuk Columnar Transposition")

class PipelineDecryptRequest(BaseModel):
    ciphertext: str = Field(..., description="Cipherteks yang akan didekripsi")
    playfair_key: str = Field("SECRET", description="Kata kunci untuk Playfair Cipher")
    vigenere_key: str = Field("CRYPTO", description="Kata kunci untuk Vigenère Cipher")
    columnar_key: str = Field("CIPHER", description="Kata kunci untuk Columnar Transposition")
    original_plaintext: Optional[str] = Field(None, description="Plainteks asli untuk validasi verifikasi 100% identik")

class SingleEncryptRequest(BaseModel):
    algorithm: str = Field(..., description="Pilihan algoritma: 'playfair' | 'vigenere' | 'columnar'")
    text: str = Field(..., description="Teks yang akan diproses")
    key: str = Field(..., description="Kata kunci algoritma")

class CryptanalysisRequest(BaseModel):
    text: str = Field(..., description="Teks yang akan dianalisis secara statistik")

# === Endpoints API ===

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AetherCrypt Backend", "version": "1.0.0"}

@app.get("/api/vigenere-tableau")
def vigenere_tableau():
    """Mengembalikan matriks bujursangkar Vigenère 26x26 untuk visualizer"""
    return {"tableau": get_vigenere_tableau()}

@app.post("/api/pipeline/encrypt")
def api_pipeline_encrypt(req: PipelineEncryptRequest):
    """Menjalankan Super-Enkripsi 3 Tahap: Playfair -> Vigenère -> Columnar"""
    try:
        result = super_encrypt(
            plaintext=req.plaintext,
            playfair_key=req.playfair_key,
            vigenere_key=req.vigenere_key,
            columnar_key=req.columnar_key
        )
        # Hitung kriptanalisis untuk plainteks dan cipherteks
        clean_p = "".join(ch for ch in req.plaintext.upper() if ch.isalpha())
        stats_plain = analyze_text(clean_p)
        stats_cipher = analyze_text(result["final_ciphertext"])

        return {
            "success": True,
            **result,
            "analysis": {
                "plaintext": stats_plain,
                "ciphertext": stats_cipher
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/pipeline/decrypt")
def api_pipeline_decrypt(req: PipelineDecryptRequest):
    """Menjalankan Super-Dekripsi 3 Tahap: Inv-Columnar -> Inv-Vigenère -> Inv-Playfair"""
    try:
        result = super_decrypt(
            ciphertext=req.ciphertext,
            playfair_key=req.playfair_key,
            vigenere_key=req.vigenere_key,
            columnar_key=req.columnar_key,
            original_plaintext=req.original_plaintext
        )
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/single/encrypt")
def api_single_encrypt(req: SingleEncryptRequest):
    """Menjalankan enkripsi mandiri pada salah satu algoritma"""
    algo = req.algorithm.lower()
    try:
        if algo == "playfair":
            res = playfair_encrypt(req.text, req.key)
        elif algo == "vigenere":
            res = vigenere_encrypt(req.text, req.key)
        elif algo == "columnar":
            res = columnar_encrypt(req.text, req.key)
        else:
            raise HTTPException(status_code=400, detail=f"Algoritma '{req.algorithm}' tidak dikenali.")
        return {"success": True, "algorithm": algo, "data": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/single/decrypt")
def api_single_decrypt(req: SingleEncryptRequest):
    """Menjalankan dekripsi mandiri pada salah satu algoritma"""
    algo = req.algorithm.lower()
    try:
        if algo == "playfair":
            res = playfair_decrypt(req.text, req.key)
        elif algo == "vigenere":
            res = vigenere_decrypt(req.text, req.key)
        elif algo == "columnar":
            res = columnar_decrypt(req.text, req.key)
        else:
            raise HTTPException(status_code=400, detail=f"Algoritma '{req.algorithm}' tidak dikenali.")
        return {"success": True, "algorithm": algo, "data": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/cryptanalysis")
def api_cryptanalysis(req: CryptanalysisRequest):
    """Menghitung distribusi frekuensi, IC, dan evaluasi keamanan statistik"""
    try:
        res = analyze_text(req.text)
        return {"success": True, "analysis": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
