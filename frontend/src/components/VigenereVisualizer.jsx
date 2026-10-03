import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function VigenereVisualizer({ stageData }) {
  if (!stageData) {
    return (
      <div className="studio-viz-card" style={{ textAlign: 'center', padding: '40px', color: '#7A756D' }}>
        Jalankan enkripsi untuk menampilkan analisis Vigenère Cipher.
      </div>
    );
  }

  const { input = '', output = '', expanded_key = '', steps = [] } = stageData;
  const [currentStepIdx, setCurrentStepIdx] = useState(0);

  const activeStep = steps[currentStepIdx] || null;

  return (
    <div className="studio-viz-card">
      {/* Header Bar */}
      <div className="viz-card-header">
        <div>
          <div className="viz-stage-tag">
            <div className="viz-tag-bar" />
            <span className="viz-tag-label">TAHAP 2 • SUBSTITUSI POLIALFABETIK</span>
          </div>
          <h3 className="viz-card-title">Vigenère Cipher (Modulo 26)</h3>
          <p className="viz-card-desc">
            Persamaan Enkripsi: Cᵢ = (Pᵢ + Kᵢ) mod 26 | Pergeseran abjad berulang
          </p>
        </div>

        {/* Step Controller */}
        {steps.length > 0 && (
          <div className="viz-step-controller">
            <button
              onClick={() => setCurrentStepIdx((prev) => Math.max(0, prev - 1))}
              disabled={currentStepIdx === 0}
              className="viz-step-btn"
              title="Karakter Sebelumnya"
            >
              <ChevronLeft style={{ width: '15px', height: '15px' }} />
            </button>
            <span className="viz-step-counter">
              Karakter {currentStepIdx + 1} / {steps.length}
            </span>
            <button
              onClick={() => setCurrentStepIdx((prev) => Math.min(steps.length - 1, prev + 1))}
              disabled={currentStepIdx === steps.length - 1}
              className="viz-step-btn"
              title="Karakter Berikutnya"
            >
              <ChevronRight style={{ width: '15px', height: '15px' }} />
            </button>
          </div>
        )}
      </div>

      {/* Alignment Ribbon */}
      <div className="vigenere-ribbon-card">
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '11px', fontWeight: 800, color: '#7A756D', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
          Penyelarasan Teks & Kunci Periodik (Key Expansion)
        </span>

        <div className="ribbon-scroll-track">
          <div className="ribbon-columns-flex">
            {input.split('').map((ch, idx) => {
              const isActive = idx === currentStepIdx;
              return (
                <div
                  key={idx}
                  onClick={() => setCurrentStepIdx(idx)}
                  className={`ribbon-column-pill ${isActive ? 'active' : ''}`}
                >
                  <span className="ribbon-col-idx">#{idx + 1}</span>
                  <span className="ribbon-col-p">{ch}</span>
                  <span className="ribbon-col-k">{expanded_key[idx] || '-'}</span>
                  <span className="ribbon-col-c">{output[idx] || '-'}</span>
                </div>
              );
            })}
          </div>
        </div>

        <div className="ribbon-legend-bar">
          <span>Baris 1: Plainteks (P)</span>
          <span style={{ color: '#B45309', fontWeight: 800 }}>Baris 2: Kunci (K)</span>
          <span style={{ color: '#059669', fontWeight: 800 }}>Baris 3: Cipherteks (C)</span>
        </div>
      </div>

      {/* Triad Calculation Details */}
      {activeStep && (
        <div className="vigenere-calc-triad">
          <div className="triad-card">
            <span className="triad-card-label">Plainteks (Pᵢ)</span>
            <div className="triad-card-char">{activeStep.p_char}</div>
            <span className="triad-card-sub">Indeks Alfabet: {activeStep.p_val}</span>
          </div>

          <div className="triad-card">
            <span className="triad-card-label" style={{ color: '#B45309' }}>Kunci Periodik (Kᵢ)</span>
            <div className="triad-card-char" style={{ color: '#B45309' }}>{activeStep.k_char}</div>
            <span className="triad-card-sub" style={{ color: '#92400E' }}>Indeks Kunci: {activeStep.k_val}</span>
          </div>

          <div className="triad-card">
            <span className="triad-card-label" style={{ color: '#059669' }}>Cipherteks (Cᵢ)</span>
            <div className="triad-card-char" style={{ color: '#059669' }}>{activeStep.c_char}</div>
            <span className="triad-card-sub" style={{ color: '#047857', fontWeight: 800 }}>{activeStep.formula}</span>
          </div>
        </div>
      )}
    </div>
  );
}
