import React, { useState, useEffect } from 'react';
import Scene3DCanvas from './components/Scene3DCanvas';
import StudioModal from './components/StudioModal';
import { ChevronLeft, ChevronRight, Lock, KeyRound, Sparkles } from 'lucide-react';

const sceneData = [
  {
    sceneIdx: 0,
    shortName: "CRYPTEX",
    mainTitle: "AetherCrypt.",
    subTitle: "Super-Enkripsi Multi-Lapis.",
    desc: "Silinder Sandi Da Vinci (Cryptex). Implementasi murni aljabar klasik tanpa library kriptografi pihak ketiga: Playfair 5×5, Vigenère Modulo 26, dan Columnar Transposition.",
    align: "left"
  },
  {
    sceneIdx: 1,
    shortName: "PLAYFAIR",
    mainTitle: "Tahap 1.",
    subTitle: "Playfair Cipher.",
    desc: "Papan ketik mekanikal Enigma menerima karakter pesan. Teks diproses per pasangan bigram pada matriks 5×5 untuk mereduksi frekuensi statistik huruf.",
    align: "right" // Khusus scene 2 (tahap 1), teks pindah ke kanan agar variatif
  },
  {
    sceneIdx: 2,
    shortName: "VIGENÈRE",
    mainTitle: "Tahap 2.",
    subTitle: "Vigenère Cipher.",
    desc: "Roda rotor Enigma berputar dinamis mengubah jalur sandi. Persamaan aritmatika Cᵢ = (Pᵢ + Kᵢ) mod 26 melakukan pergeseran periodik berlapis.",
    align: "left"
  },
  {
    sceneIdx: 3,
    shortName: "COLUMNAR",
    mainTitle: "Tahap 3.",
    subTitle: "Columnar Transposition.",
    desc: "Papan kabel Plugboard mengacak sambungan karakter secara acak. Transposisi Kolom mendifusikan posisi spasial karakter teks.",
    align: "right"
  },
  {
    sceneIdx: 4,
    shortName: "VALIDASI",
    mainTitle: "Kunci Validasi.",
    subTitle: "Reversibilitas 100%.",
    desc: "Seperti brankas mekanikal yang hanya terbuka dengan kunci presisi, pipeline super-enkripsi menjamin dekripsi balik P → C → P' identik 100%.",
    align: "left"
  }
];

export default function App() {
  // Scene State (0 - 4)
  const [currentScene, setCurrentScene] = useState(0);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Kripto Input State
  const [plaintext, setPlaintext] = useState('TEMUI SAYA DI LABORATORIUM KRIPTOGRAFI MALAM INI');
  const [playfairKey, setPlayfairKey] = useState('UNIVERSITAS');
  const [vigenereKey, setVigenereKey] = useState('SOEDIRMAN');
  const [columnarKey, setColumnarKey] = useState('INFORMATIKA');

  // Execution Results State
  const [isProcessing, setIsProcessing] = useState(false);
  const [pipelineResult, setPipelineResult] = useState(null);
  const [decryptionResult, setDecryptionResult] = useState(null);
  const [copied, setCopied] = useState(false);

  // Auto execute initial encryption on mount
  useEffect(() => {
    handleSuperEncrypt();
  }, []);

  const handleSuperEncrypt = async () => {
    setIsProcessing(true);
    setDecryptionResult(null);

    try {
      const resp = await fetch('/api/pipeline/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plaintext: plaintext || 'KRIPTOGRAFI',
          playfair_key: playfairKey || 'SECRET',
          vigenere_key: vigenereKey || 'CRYPTO',
          columnar_key: columnarKey || 'CIPHER',
        }),
      });
      const data = await resp.json();
      if (data.success) {
        setPipelineResult(data);
      } else {
        alert('Gagal enkripsi: ' + (data.detail || 'Terjadi kesalahan'));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSuperDecrypt = async () => {
    if (!pipelineResult || !pipelineResult.final_ciphertext) {
      alert('Silakan lakukan enkripsi terlebih dahulu.');
      return;
    }

    setIsProcessing(true);
    try {
      const resp = await fetch('/api/pipeline/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ciphertext: pipelineResult.final_ciphertext,
          playfair_key: playfairKey,
          vigenere_key: vigenereKey,
          columnar_key: columnarKey,
          original_plaintext: plaintext,
        }),
      });
      const data = await resp.json();
      if (data.success) {
        setDecryptionResult(data);
      } else {
        alert('Gagal dekripsi: ' + (data.detail || 'Terjadi kesalahan'));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      setPlaintext(event.target.result);
    };
    reader.readAsText(file);
  };

  const handleDownload = (text, filename) => {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleNextScene = () => {
    setCurrentScene((prev) => (prev + 1) % sceneData.length);
  };

  const handlePrevScene = (e) => {
    e.stopPropagation();
    setCurrentScene((prev) => (prev - 1 + sceneData.length) % sceneData.length);
  };

  const handleNextSceneBtn = (e) => {
    e.stopPropagation();
    handleNextScene();
  };

  const currentInfo = sceneData[currentScene] || sceneData[0];

  return (
    <div className="relative w-full h-screen overflow-hidden bg-[var(--bg-primary)] text-[var(--text-primary)] font-['Inter',sans-serif] select-none">
      
      {/* Background Radial Ambient Glows matching D:\spk */}
      <div className="ambient-glow-1"></div>
      <div className="ambient-glow-2"></div>

      {/* 3D Canvas Fullscreen Background */}
      <Scene3DCanvas currentScene={currentScene} isProcessing={isProcessing} />

      {/* Click Catcher for Background Navigation (Klik di mana saja pada layar luar tombol) */}
      <div 
        className="absolute inset-0 z-[5] cursor-pointer"
        onClick={handleNextScene}
        title="Klik di mana saja untuk berganti scene artefak"
      />

      {/* Main HUD Overlay Layer with Fixed Screen Edge Margins matching D:\spk */}
      <div className="absolute top-8 bottom-8 left-8 right-8 md:top-12 md:bottom-12 md:left-14 md:right-14 pointer-events-none flex flex-col justify-between z-10">
        
        {/* Top Header Bar */}
        <header className="w-full flex justify-between items-center pointer-events-auto">
          <div 
            onClick={() => setCurrentScene(0)}
            className="cursor-pointer"
          >
            <span className="font-heading font-black text-2xl md:text-3xl tracking-tighter text-[var(--text-primary)]">
              AetherCrypt.
            </span>
          </div>

          <div className="flex items-center">
            <button 
              onClick={(e) => {
                e.stopPropagation();
                setIsModalOpen(true);
              }}
              className="mulai-btn shadow-lg"
            >
              <span>MULAI</span>
            </button>
          </div>
        </header>

        {/* Dynamic Minimalist HUD (Kiri / Kanan Variatif antar-Scene) */}
        <main className={`max-w-xl pointer-events-auto z-20 space-y-3 pb-2 transition-all duration-500 ${
          currentInfo.align === 'right' 
            ? 'text-right ml-auto self-end' 
            : 'text-left mr-auto self-start'
        }`}>
          <div>
            <h1 className="font-heading font-black text-4xl sm:text-5xl lg:text-6xl tracking-tight text-[var(--text-primary)] leading-[0.92]">
              {currentInfo.mainTitle}
            </h1>
            <h2 className="font-heading font-black text-4xl sm:text-5xl lg:text-6xl tracking-tight text-[#8A8680] leading-[0.92] mt-1">
              {currentInfo.subTitle}
            </h2>
          </div>

          <p className={`text-xs sm:text-sm md:text-[15px] text-[var(--text-muted)] font-normal leading-relaxed max-w-lg pt-1 ${
            currentInfo.align === 'right' ? 'ml-auto' : 'mr-auto'
          }`}>
            {currentInfo.desc}
          </p>
        </main>

        {/* Bottom Navigation Scene Switcher & Stepper */}
        <footer className="w-full flex justify-between items-center pointer-events-auto pt-2">
          
          {/* Minimalist Geometric Scene Stepper (Without Numbers) */}
          <div className="scene-stepper-capsule">
            {sceneData.map((s, idx) => {
              const isActive = currentScene === idx;
              return (
                <button
                  key={idx}
                  onClick={(e) => {
                    e.stopPropagation();
                    setCurrentScene(idx);
                  }}
                  className={`scene-dot-btn ${isActive ? 'active' : ''}`}
                  title={`Artefak ${idx + 1}: ${s.shortName || s.mainTitle}`}
                >
                  <div className="scene-dot-track" />
                </button>
              );
            })}
          </div>

          {/* Previous / Next Arrow Capsule */}
          <div className="scene-arrows-capsule">
            <button
              onClick={handlePrevScene}
              className="scene-arrow-btn"
              title="Artefak Sebelumnya"
            >
              <ChevronLeft style={{ width: '15px', height: '15px' }} />
            </button>
            <span className="scene-counter-label">
              0{currentScene + 1} / 0{sceneData.length}
            </span>
            <button
              onClick={handleNextSceneBtn}
              className="scene-arrow-btn"
              title="Artefak Berikutnya"
            >
              <ChevronRight style={{ width: '15px', height: '15px' }} />
            </button>
          </div>

        </footer>

      </div>

      {/* Studio Modal Dialog (Triggered by Button "MULAI") */}
      <StudioModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        plaintext={plaintext}
        setPlaintext={setPlaintext}
        playfairKey={playfairKey}
        setPlayfairKey={setPlayfairKey}
        vigenereKey={vigenereKey}
        setVigenereKey={setVigenereKey}
        columnarKey={columnarKey}
        setColumnarKey={setColumnarKey}
        handleSuperEncrypt={handleSuperEncrypt}
        handleSuperDecrypt={handleSuperDecrypt}
        isProcessing={isProcessing}
        pipelineResult={pipelineResult}
        decryptionResult={decryptionResult}
        handleFileUpload={handleFileUpload}
        handleDownload={handleDownload}
        handleCopy={handleCopy}
        copied={copied}
      />

    </div>
  );
}
