import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function PlayfairVisualizer({ stageData }) {
  if (!stageData || !stageData.matrix) {
    return (
      <div className="studio-viz-card" style={{ textAlign: 'center', padding: '40px', color: '#7A756D' }}>
        Jalankan enkripsi untuk menampilkan matriks dan langkah Playfair Cipher.
      </div>
    );
  }

  const { matrix, steps = [], input = '', output = '' } = stageData;
  const [currentStepIdx, setCurrentStepIdx] = useState(0);

  const activeStep = steps[currentStepIdx] || null;

  const isInputCell = (r, c) => {
    if (!activeStep || !activeStep.pos_in) return false;
    return activeStep.pos_in.some(([row, col]) => row === r && col === c);
  };

  const isOutputCell = (r, c) => {
    if (!activeStep || !activeStep.pos_out) return false;
    return activeStep.pos_out.some(([row, col]) => row === r && col === c);
  };

  return (
    <div className="studio-viz-card">
      {/* Header Bar */}
      <div className="viz-card-header">
        <div>
          <div className="viz-stage-tag">
            <div className="viz-tag-bar" />
            <span className="viz-tag-label">TAHAP 1 • SUBSTITUSI POLIGRAM</span>
          </div>
          <h3 className="viz-card-title">Playfair Cipher (Matriks 5×5)</h3>
          <p className="viz-card-desc">
            Memetakan pasangan huruf (bigram) dengan penggabungan huruf 'J' menjadi 'I'
          </p>
        </div>

        {/* Step Controller */}
        {steps.length > 0 && (
          <div className="viz-step-controller">
            <button
              onClick={() => setCurrentStepIdx((prev) => Math.max(0, prev - 1))}
              disabled={currentStepIdx === 0}
              className="viz-step-btn"
              title="Langkah Sebelumnya"
            >
              <ChevronLeft style={{ width: '15px', height: '15px' }} />
            </button>
            <span className="viz-step-counter">
              Bigram {currentStepIdx + 1} / {steps.length}
            </span>
            <button
              onClick={() => setCurrentStepIdx((prev) => Math.min(steps.length - 1, prev + 1))}
              disabled={currentStepIdx === steps.length - 1}
              className="viz-step-btn"
              title="Langkah Berikutnya"
            >
              <ChevronRight style={{ width: '15px', height: '15px' }} />
            </button>
          </div>
        )}
      </div>

      {/* Main Grid Layout */}
      <div className="playfair-layout-grid">
        {/* 5x5 Matrix Display */}
        <div className="playfair-matrix-box">
          <div className="playfair-5x5-grid">
            {matrix.map((row, rIdx) =>
              row.map((char, cIdx) => {
                const inActive = isInputCell(rIdx, cIdx);
                const outActive = isOutputCell(rIdx, cIdx);

                let cellClass = 'pf-cell';
                if (inActive) cellClass += ' cell-in';
                else if (outActive) cellClass += ' cell-out';

                return (
                  <div key={`${rIdx}-${cIdx}`} className={cellClass}>
                    {char}
                  </div>
                );
              })
            )}
          </div>

          <div className="pf-legend-row">
            <span className="pf-legend-item">
              <span className="pf-legend-dot input" /> Huruf Input
            </span>
            <span className="pf-legend-item">
              <span className="pf-legend-dot output" /> Hasil Sandi
            </span>
          </div>
        </div>

        {/* Step Breakdown & Transformation Panel */}
        <div className="playfair-steps-panel">
          {activeStep && (
            <div className="playfair-transform-card">
              <div className="transform-card-header">
                <span className="transform-label">Transformasi Pasangan</span>
                <span className="transform-rule-badge">
                  {activeStep.rule ? activeStep.rule.replace(/_/g, ' ') : 'ATURAN PLAYFAIR'}
                </span>
              </div>

              <div className="transform-pair-visual">
                <div className="pair-block">
                  <span className="pair-label">Input</span>
                  <div className="pair-bigram-box">{activeStep.in}</div>
                </div>

                <span className="pair-arrow">➔</span>

                <div className="pair-block">
                  <span className="pair-label">Output</span>
                  <div className="pair-bigram-box output">{activeStep.out}</div>
                </div>
              </div>

              <div className="transform-explanation">
                {activeStep.description}
              </div>
            </div>
          )}

          <div className="playfair-io-summary">
            <div className="io-summary-card">
              <span className="io-summary-label">Input Plainteks:</span>
              <span className="io-summary-val">{input}</span>
            </div>
            <div className="io-summary-card">
              <span className="io-summary-label">Output Tahap 1:</span>
              <span className="io-summary-val highlight">{output}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
