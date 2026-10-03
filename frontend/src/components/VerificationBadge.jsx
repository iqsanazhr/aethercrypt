import React from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';

export default function VerificationBadge({ verification }) {
  if (!verification) return null;

  const { is_identical, match_percentage, original_normalized, decrypted_result } = verification;

  return (
    <div className={`verification-card-box ${!is_identical ? 'error' : ''}`}>
      <div className="verification-header-row">
        <div className="verification-info-group">
          <div className={`verification-icon-circle ${!is_identical ? 'error' : ''}`}>
            {is_identical ? (
              <CheckCircle2 style={{ width: '22px', height: '22px' }} />
            ) : (
              <XCircle style={{ width: '22px', height: '22px' }} />
            )}
          </div>

          <div>
            <div className="verification-title-wrap">
              <h4 className="verification-main-title">
                {is_identical
                  ? 'Validasi Kebenaran: 100% Identik & Terverifikasi'
                  : 'Validasi Kebenaran: Perbedaan Terdeteksi'}
              </h4>
              <span className={`verification-match-pill ${!is_identical ? 'error' : ''}`}>
                {match_percentage}% MATCH
              </span>
            </div>
            <p className="verification-desc-text">
              {is_identical
                ? 'Hasil dekripsi balik membuktikan rumus matematika algoritma bekerja sempurna secara bolak-balik (Round-Trip Verified).'
                : 'Periksa kembali kesesuaian kata kunci yang dimasukkan.'}
            </p>
          </div>
        </div>

        <div className="verification-formula-box">
          <span className="formula-label">Formula Verifikasi:</span>
          <span className="formula-code">P ➔ Enc ➔ Dec ➔ P' ≡ P</span>
        </div>
      </div>

      {/* Comparison Grid */}
      <div className="verification-compare-grid">
        <div className="compare-box input-side">
          <span className="compare-box-label">Plainteks Normalisasi (Input):</span>
          <span className="compare-box-val">{original_normalized}</span>
        </div>
        <div className="compare-box output-side">
          <span className="compare-box-label">Hasil Dekripsi Terakhir (Output):</span>
          <span className="compare-box-val">{decrypted_result}</span>
        </div>
      </div>
    </div>
  );
}
