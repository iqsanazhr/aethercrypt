import React, { useState } from 'react';

export default function ColumnarVisualizer({ stageData }) {
  if (!stageData || !stageData.grid) {
    return (
      <div className="studio-viz-card" style={{ textAlign: 'center', padding: '40px', color: '#7A756D' }}>
        Jalankan enkripsi untuk menampilkan grid Transposisi Kolom.
      </div>
    );
  }

  const { grid = [], col_order = [], ciphertext_cols = [], output = '' } = stageData;
  const [highlightCol, setHighlightCol] = useState(null);

  return (
    <div className="studio-viz-card">
      {/* Header Bar */}
      <div className="viz-card-header">
        <div>
          <div className="viz-stage-tag">
            <div className="viz-tag-bar" />
            <span className="viz-tag-label">TAHAP 3 • TRANSPOSISI GEOMETRIS</span>
          </div>
          <h3 className="viz-card-title">Columnar Transposition (Transposisi Kolom)</h3>
          <p className="viz-card-desc">
            Mengacak posisi spasial huruf berdasarkan permutasi urutan abjad kata kunci
          </p>
        </div>

        <span className="card-badge-counter">
          {col_order.length} Kolom × {grid.length} Baris
        </span>
      </div>

      {/* Main Grid Layout */}
      <div className="columnar-layout-grid">
        {/* Matrix Display */}
        <div className="columnar-matrix-box">
          {/* Header Columns Priority */}
          <div className="col-header-row">
            {col_order.map((origColIdx, readPriority) => {
              const colData = ciphertext_cols.find((c) => c.col_index === readPriority);
              const isSelected = highlightCol === readPriority;

              return (
                <div
                  key={readPriority}
                  onMouseEnter={() => setHighlightCol(readPriority)}
                  onMouseLeave={() => setHighlightCol(null)}
                  className={`col-header-cell ${isSelected ? 'highlight' : ''}`}
                >
                  <span className="col-priority-badge">#{readPriority + 1}</span>
                  <span className="col-key-letter">{colData?.key_char || '?'}</span>
                  <span className="col-priority-badge">Kol {readPriority}</span>
                </div>
              );
            })}
          </div>

          {/* Grid Cells */}
          <div className="col-body-rows">
            {grid.map((row, rIdx) => (
              <div key={rIdx} className="col-body-row">
                {row.map((char, cIdx) => {
                  const isSelected = highlightCol === cIdx;
                  return (
                    <div
                      key={`${rIdx}-${cIdx}`}
                      className={`col-body-cell ${isSelected ? 'highlight' : ''}`}
                    >
                      {char}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        </div>

        {/* Priority Order List & Result */}
        <div className="columnar-reads-stack">
          <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '11px', fontWeight: 800, color: '#7A756D', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            Urutan Pembacaan Kolom (Prioritas Alfabetik)
          </span>

          <div className="columnar-reads-list">
            {ciphertext_cols.map((col, idx) => {
              const isSelected = highlightCol === col.col_index;
              return (
                <div
                  key={idx}
                  onMouseEnter={() => setHighlightCol(col.col_index)}
                  onMouseLeave={() => setHighlightCol(null)}
                  className={`col-read-item ${isSelected ? 'highlight' : ''}`}
                >
                  <div className="col-read-left">
                    <span className="col-read-num">{idx + 1}</span>
                    <span className="col-read-name">
                      Kunci '{col.key_char}' (Kolom {col.col_index})
                    </span>
                  </div>
                  <span className="col-read-chars">{col.chars}</span>
                </div>
              );
            })}
          </div>

          <div className="io-summary-card" style={{ marginTop: '6px' }}>
            <span className="io-summary-label">Hasil Super-Cipherteks Akhir:</span>
            <span className="io-summary-val highlight" style={{ fontSize: '14px', marginTop: '4px' }}>
              {output}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
