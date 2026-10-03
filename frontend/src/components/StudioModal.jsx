import React, { useState } from 'react';
import { 
  X, Minus, Maximize2, Minimize2, Lock, Unlock, Upload, Download, Copy, Check, RefreshCw, 
  ChevronRight, ChevronLeft, ArrowRight, ShieldCheck, FileText, KeyRound
} from 'lucide-react';
import './StudioModal.css';
import PlayfairVisualizer from './PlayfairVisualizer';
import VigenereVisualizer from './VigenereVisualizer';
import ColumnarVisualizer from './ColumnarVisualizer';
import CryptanalysisLab from './CryptanalysisLab';
import VerificationBadge from './VerificationBadge';

export default function StudioModal({
  isOpen,
  onClose,
  plaintext,
  setPlaintext,
  playfairKey,
  setPlayfairKey,
  vigenereKey,
  setVigenereKey,
  columnarKey,
  setColumnarKey,
  handleSuperEncrypt,
  handleSuperDecrypt,
  isProcessing,
  pipelineResult,
  decryptionResult,
  handleFileUpload,
  handleDownload,
  handleCopy,
  copied
}) {
  // Modal Section: 'input' | 'output' | 'visualizer'
  const [modalSection, setModalSection] = useState('input');
  const [activeVisualizerTab, setActiveVisualizerTab] = useState('pipeline');
  const [isMaximized, setIsMaximized] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);

  if (!isOpen) return null;

  const onExecuteEncrypt = async () => {
    await handleSuperEncrypt();
    setModalSection('output');
  };

  // Minimized floating dock
  if (isMinimized) {
    return (
      <div 
        className="studio-minimized-dock"
        onClick={() => setIsMinimized(false)}
        title="Klik untuk memulihkan Studio Modal"
      >
        <div className="studio-modal-traffic-lights" style={{ pointerEvents: 'none' }}>
          <div className="traffic-dot red" />
          <div className="traffic-dot yellow" />
          <div className="traffic-dot green" />
        </div>
        <span className="dock-title">
          AetherCrypt Studio ({modalSection === 'input' ? '01 Input' : modalSection === 'output' ? '02 Keluaran' : '03 Visualizer'})
        </span>
        <button 
          type="button" 
          className="dock-restore-btn"
          onClick={(e) => {
            e.stopPropagation();
            setIsMinimized(false);
          }}
        >
          <Maximize2 style={{ width: '11px', height: '11px' }} />
          <span>Pulihkan</span>
        </button>
      </div>
    );
  }

  return (
    <div className="studio-modal-backdrop">

      {/* Main Glassmorphic Modal Dialog */}
      <div className={`studio-modal-window ${isMaximized ? 'maximized' : ''}`}>
        
        {/* =========================================================================
            TOP HEADER: macOS Window Bar & Step Navigation
           ========================================================================= */}
        <div className="studio-modal-header">
          
          {/* Left: Window Controls + Badge */}
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div className="studio-modal-traffic-lights">
              {/* Red Dot: Close */}
              <button 
                type="button"
                onClick={() => {
                  setIsMinimized(false);
                  setIsMaximized(false);
                  onClose();
                }}
                className="traffic-dot red"
                title="Tutup Modal"
              >
                <X style={{ width: '8px', height: '8px', color: '#4D0000' }} />
              </button>

              {/* Yellow Dot: Minimize */}
              <button 
                type="button"
                onClick={() => setIsMinimized(true)}
                className="traffic-dot yellow"
                title="Perkecil ke Dock (Minimize)"
              >
                <Minus style={{ width: '8px', height: '8px', color: '#664400' }} />
              </button>

              {/* Green Dot: Maximize / Restore */}
              <button 
                type="button"
                onClick={() => setIsMaximized(!isMaximized)}
                className="traffic-dot green"
                title={isMaximized ? "Kembalikan Ukuran Jendela (Restore)" : "Perbesar Penuh (Maximize)"}
              >
                {isMaximized ? (
                  <Minimize2 style={{ width: '7px', height: '7px', color: '#003300' }} />
                ) : (
                  <Maximize2 style={{ width: '7px', height: '7px', color: '#003300' }} />
                )}
              </button>
            </div>

            <div className="studio-modal-header-title">
              <span className="header-pulse-dot" />
              <span>
                {modalSection === 'input' && 'Studio Parameter • Tahap 1/3'}
                {modalSection === 'output' && 'Keluaran Sandi • Tahap 2/3'}
                {modalSection === 'visualizer' && 'Laboratorium Forensik • Tahap 3/3'}
              </span>
            </div>
          </div>

          {/* Right: Step Segmented Pills (Right 'X' Close Button Removed) */}
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div className="studio-step-nav">
              <button
                onClick={() => setModalSection('input')}
                className={`step-nav-btn ${modalSection === 'input' ? 'active' : ''}`}
              >
                01 Input
              </button>

              <button
                onClick={() => {
                  if (pipelineResult) setModalSection('output');
                }}
                disabled={!pipelineResult}
                className={`step-nav-btn ${modalSection === 'output' ? 'active' : ''}`}
              >
                02 Keluaran
              </button>

              <button
                onClick={() => {
                  if (pipelineResult) setModalSection('visualizer');
                }}
                disabled={!pipelineResult}
                className={`step-nav-btn ${modalSection === 'visualizer' ? 'active' : ''}`}
              >
                03 Visualizer
              </button>
            </div>
          </div>
        </div>

        {/* =========================================================================
            MODAL SCROLLABLE BODY
           ========================================================================= */}
        <div className="studio-modal-body">

          {/* ---------------------------------------------------------------------
              SECTION 1: INPUT STUDIO PARAMETER
             --------------------------------------------------------------------- */}
          {modalSection === 'input' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              
              {/* Title & Quick Actions */}
              <div className="studio-title-row">
                <div>
                  <h2 className="studio-main-heading">
                    Parameter Super-Enkripsi.
                  </h2>
                  <div className="studio-sub-heading">
                    Pipeline 3 Lapis: Playfair (5×5) → Vigenère (Mod 26) → Columnar Transposition
                  </div>
                </div>

                <div className="studio-quick-actions">
                  <label className="action-pill-btn">
                    <Upload style={{ width: '14px', height: '14px', color: '#7A756D' }} />
                    <span>Upload .txt</span>
                    <input type="file" accept=".txt" onChange={handleFileUpload} style={{ display: 'none' }} />
                  </label>

                  <button
                    type="button"
                    onClick={() => {
                      setPlaintext('SERANGAN SIBER TERDETEKSI PADA JARINGAN SISTEM AKADEMIK KAMPUS');
                      setPlayfairKey('UNSOED');
                      setVigenereKey('PURWOKERTO');
                      setColumnarKey('INFORMATIKA');
                    }}
                    className="action-pill-btn"
                  >
                    <RefreshCw style={{ width: '14px', height: '14px', color: '#7A756D' }} />
                    <span>Preset Kasus</span>
                  </button>
                </div>
              </div>

              {/* Two Column Grid */}
              <div className="studio-two-col">
                
                {/* Left Column: Plaintext Input Box */}
                <div className="studio-card-white">
                  <div className="card-header-bar">
                    <span className="card-title-text">
                      <FileText style={{ width: '16px', height: '16px', color: '#1D1C1B' }} />
                      Pesan Plainteks (Input)
                    </span>
                    <span className="card-badge-counter">
                      {plaintext.length} Karakter
                    </span>
                  </div>

                  <textarea
                    rows={8}
                    value={plaintext}
                    onChange={(e) => setPlaintext(e.target.value)}
                    placeholder="Ketik atau tempel teks rahasia yang akan dienkripsi..."
                    className="studio-textarea-input"
                  />
                  
                  <div className="card-footer-note">
                    <span>* Otomatis diformat dan dibersihkan pada tahap Playfair</span>
                    <span style={{ fontWeight: 800, color: '#1D1C1B' }}>ASCII PLAINTEXT</span>
                  </div>
                </div>

                {/* Right Column: 3 Stepped Keys */}
                <div className="studio-keys-stack">
                  
                  {/* Key 1: Playfair */}
                  <div className="studio-key-card">
                    <div className="key-card-header">
                      <div className="key-card-left">
                        <span className="key-badge-num">1</span>
                        <span className="key-card-name">Kunci Playfair (Matriks 5×5)</span>
                      </div>
                      <span className="key-algorithm-badge">Substitusi Poligram</span>
                    </div>
                    <input
                      type="text"
                      value={playfairKey}
                      onChange={(e) => setPlayfairKey(e.target.value.toUpperCase())}
                      placeholder="Contoh: UNIVERSITAS"
                      className="studio-text-input"
                    />
                  </div>

                  {/* Key 2: Vigenere */}
                  <div className="studio-key-card">
                    <div className="key-card-header">
                      <div className="key-card-left">
                        <span className="key-badge-num">2</span>
                        <span className="key-card-name">Kunci Vigenère (Modulo 26)</span>
                      </div>
                      <span className="key-algorithm-badge">Substitusi Periodik</span>
                    </div>
                    <input
                      type="text"
                      value={vigenereKey}
                      onChange={(e) => setVigenereKey(e.target.value.toUpperCase())}
                      placeholder="Contoh: SOEDIRMAN"
                      className="studio-text-input"
                    />
                  </div>

                  {/* Key 3: Columnar */}
                  <div className="studio-key-card">
                    <div className="key-card-header">
                      <div className="key-card-left">
                        <span className="key-badge-num">3</span>
                        <span className="key-card-name">Kunci Columnar Transposition</span>
                      </div>
                      <span className="key-algorithm-badge">Permutasi Kolom</span>
                    </div>
                    <input
                      type="text"
                      value={columnarKey}
                      onChange={(e) => setColumnarKey(e.target.value.toUpperCase())}
                      placeholder="Contoh: INFORMATIKA"
                      className="studio-text-input"
                    />
                  </div>

                </div>

              </div>

            </div>
          )}

          {/* ---------------------------------------------------------------------
              SECTION 2: OUTPUT KELUARAN SANDI
             --------------------------------------------------------------------- */}
          {modalSection === 'output' && pipelineResult && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              
              <div className="studio-title-row">
                <div>
                  <div className="status-badge-pill">
                    <Lock style={{ width: '13px', height: '13px' }} />
                    <span>Enkripsi Selesai • 3 Tahap Terkunci</span>
                  </div>
                  <h2 className="studio-main-heading">
                    Super-Cipherteks Terkunci.
                  </h2>
                </div>

                <div className="studio-quick-actions">
                  <button
                    onClick={() => handleCopy(pipelineResult.final_ciphertext)}
                    className="action-pill-btn"
                  >
                    {copied ? <Check style={{ width: '14px', height: '14px', color: '#10b981' }} /> : <Copy style={{ width: '14px', height: '14px', color: '#7A756D' }} />}
                    <span>{copied ? 'Tersalin' : 'Salin Sandi'}</span>
                  </button>

                  <button
                    onClick={() => handleDownload(pipelineResult.final_ciphertext, 'super_ciphertext.txt')}
                    className="action-pill-btn"
                  >
                    <Download style={{ width: '14px', height: '14px', color: '#7A756D' }} />
                    <span>Unduh .txt</span>
                  </button>
                </div>
              </div>

              {/* Ciphertext Display Box */}
              <div className="output-ciphertext-box">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '11px', fontWeight: 800, color: '#7A756D', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
                    Cipherteks Hasil Transposisi Kolom Akhir:
                  </span>
                  <span className="card-badge-counter">
                    {pipelineResult.final_ciphertext.length} Karakter
                  </span>
                </div>
                <div className="ciphertext-inner-well">
                  {pipelineResult.final_ciphertext}
                </div>
              </div>

              {/* Verification & Integrity Status */}
              {decryptionResult ? (
                <VerificationBadge verification={decryptionResult.verification} />
              ) : (
                <div className="studio-card-white" style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: '#1D1C1B', color: '#F4F1EB', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <ShieldCheck style={{ width: '20px', height: '20px' }} />
                    </div>
                    <div>
                      <span style={{ fontWeight: 800, fontSize: '14px', color: '#1D1C1B', display: 'block' }}>
                        Validasi Reversibilitas Integritas Pesan
                      </span>
                      <span style={{ fontSize: '12px', color: '#7A756D' }}>
                        Uji dekripsi balik P → C → P' untuk membuktikan pesan pulih identik tanpa korupsi data.
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={handleSuperDecrypt}
                    disabled={isProcessing}
                    className="studio-primary-action-btn"
                    style={{ padding: '10px 24px', fontSize: '11px' }}
                  >
                    <Unlock style={{ width: '14px', height: '14px' }} />
                    <span>Uji Dekripsi & Validasi 100%</span>
                  </button>
                </div>
              )}

            </div>
          )}

          {/* ---------------------------------------------------------------------
              SECTION 3: VISUALIZER PROSES & FORENSIK
             --------------------------------------------------------------------- */}
          {modalSection === 'visualizer' && pipelineResult && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              
              <div className="studio-title-row">
                <div>
                  <h2 className="studio-main-heading">
                    Laboratorium Forensik & Visualizer.
                  </h2>
                  <div className="studio-sub-heading">
                    Telusuri matematika matriks, pergeseran abjad, dan difusi permutasi kolom
                  </div>
                </div>
              </div>

              {/* Navigation Tab Pills */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {[
                  { id: 'pipeline', label: 'Semua Tahap' },
                  { id: 'playfair', label: 'Playfair 5×5' },
                  { id: 'vigenere', label: 'Vigenère Modulo 26' },
                  { id: 'columnar', label: 'Columnar Grid' },
                  { id: 'cryptanalysis', label: 'Kriptanalisis IC & Entropi' }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveVisualizerTab(tab.id)}
                    className="action-pill-btn"
                    style={{
                      background: activeVisualizerTab === tab.id ? '#1D1C1B' : '#FFFFFF',
                      color: activeVisualizerTab === tab.id ? '#F4F1EB' : '#7A756D',
                      borderColor: activeVisualizerTab === tab.id ? '#1D1C1B' : '#D8D3C8'
                    }}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Visualizer Content Container */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {activeVisualizerTab === 'pipeline' && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    <PlayfairVisualizer stageData={pipelineResult.stages.stage1_playfair} />
                    <VigenereVisualizer stageData={pipelineResult.stages.stage2_vigenere} />
                    <ColumnarVisualizer stageData={pipelineResult.stages.stage3_columnar} />
                    <CryptanalysisLab analysisData={pipelineResult.analysis} />
                  </div>
                )}

                {activeVisualizerTab === 'playfair' && (
                  <PlayfairVisualizer stageData={pipelineResult.stages.stage1_playfair} />
                )}

                {activeVisualizerTab === 'vigenere' && (
                  <VigenereVisualizer stageData={pipelineResult.stages.stage2_vigenere} />
                )}

                {activeVisualizerTab === 'columnar' && (
                  <ColumnarVisualizer stageData={pipelineResult.stages.stage3_columnar} />
                )}

                {activeVisualizerTab === 'cryptanalysis' && (
                  <CryptanalysisLab analysisData={pipelineResult.analysis} />
                )}
              </div>

            </div>
          )}

        </div>

        {/* =========================================================================
            FIXED MODAL FOOTER
           ========================================================================= */}
        <div className="studio-modal-footer">
          
          {/* Left Footer Action */}
          <div>
            {modalSection === 'input' && (
              <span className="footer-info-text">
                Metode: Playfair (5×5) + Vigenère (Modulo 26) + Columnar Transposition
              </span>
            )}

            {modalSection === 'output' && (
              <button
                onClick={() => setModalSection('input')}
                className="action-pill-btn"
              >
                <ChevronLeft style={{ width: '14px', height: '14px', color: '#7A756D' }} />
                <span>Ulangi Parameter Input</span>
              </button>
            )}

            {modalSection === 'visualizer' && (
              <button
                onClick={() => setModalSection('output')}
                className="action-pill-btn"
              >
                <ChevronLeft style={{ width: '14px', height: '14px', color: '#7A756D' }} />
                <span>Kembali ke Hasil Sandi</span>
              </button>
            )}
          </div>

          {/* Right Footer Action */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {modalSection === 'input' && (
              <button
                onClick={onExecuteEncrypt}
                disabled={isProcessing}
                className="studio-primary-action-btn"
              >
                <Lock style={{ width: '15px', height: '15px' }} />
                <span>{isProcessing ? 'Mengenkripsi Sandi...' : 'Jalankan Super-Enkripsi 3 Tahap'}</span>
                <ArrowRight style={{ width: '15px', height: '15px' }} />
              </button>
            )}

            {modalSection === 'output' && (
              <button
                onClick={() => setModalSection('visualizer')}
                className="studio-primary-action-btn"
              >
                <span>Lihat Forensik Visualizer</span>
                <ChevronRight style={{ width: '15px', height: '15px' }} />
              </button>
            )}

            {modalSection === 'visualizer' && (
              <button
                onClick={onClose}
                className="studio-primary-action-btn"
              >
                <span>Tutup Dialog Studio</span>
              </button>
            )}
          </div>

        </div>

      </div>
    </div>
  );
}
