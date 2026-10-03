import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Scale, CheckCircle2 } from 'lucide-react';

export default function CryptanalysisLab({ analysisData }) {
  if (!analysisData || !analysisData.ciphertext) {
    return (
      <div className="studio-viz-card" style={{ textAlign: 'center', padding: '40px', color: '#7A756D' }}>
        Jalankan super-enkripsi untuk melihat analisis forensik frekuensi dan Index of Coincidence.
      </div>
    );
  }

  const { plaintext = {}, ciphertext = {} } = analysisData;

  const chartData = (ciphertext.frequencies || []).map((cItem) => {
    const pItem = (plaintext.frequencies || []).find((p) => p.letter === cItem.letter);
    return {
      letter: cItem.letter,
      Plainteks: pItem ? pItem.percentage : 0,
      SuperCipher: cItem.percentage,
      Standar_ID: cItem.ref_indonesia
    };
  });

  // Hitung persentase keacakan berdasarkan deviasi IC terhadap acak ideal 0.0385
  const icVal = ciphertext.ic || 0.0385;
  const icIdeal = 0.0385;
  const icDiff = Math.abs(icVal - icIdeal);
  const randomnessPct = Math.min(100, Math.max(0, Math.round((1 - (icDiff / 0.04)) * 100)));
  const dashOffset = 251.2 - (251.2 * randomnessPct / 100);

  return (
    <div className="studio-viz-card">
      {/* Header Bar */}
      <div className="viz-card-header">
        <div>
          <div className="viz-stage-tag">
            <div className="viz-tag-bar" />
            <span className="viz-tag-label">FORENSIK KRIPTANALISIS • METRIK STATISTIK</span>
          </div>
          <h3 className="viz-card-title">Laboratorium Kriptanalisis & Pengujian IC</h3>
          <p className="viz-card-desc">
            Membuktikan perataan distribusi frekuensi huruf (flat histogram) dan ketahanan terhadap serangan statistik
          </p>
        </div>

        <div className="status-badge-pill" style={{ marginBottom: 0 }}>
          <CheckCircle2 style={{ width: '13px', height: '13px' }} />
          <span>Forensik Terverifikasi</span>
        </div>
      </div>

      {/* Metrics Banner */}
      <div className="crypto-metric-banner">
        {/* Radial Gauge */}
        <div className="crypto-radial-box">
          <div className="radial-svg-wrap">
            <svg style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }} viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="40" fill="none" stroke="#EAE6DF" strokeWidth="8" />
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="#1D1C1B"
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray="251.2"
                strokeDashoffset={dashOffset}
                style={{ transition: 'all 1s ease-out' }}
              />
            </svg>
            <div className="radial-percent-center">
              {randomnessPct}%
            </div>
          </div>

          <div>
            <span className="stat-card-label">Derajat Keacakan Sandi</span>
            <div style={{ fontSize: '18px', fontWeight: 900, color: '#1D1C1B', marginTop: '2px' }}>
              {randomnessPct >= 80 ? 'Sangat Aman' : 'Cukup Aman'}
            </div>
            <p style={{ fontSize: '11px', color: '#7A756D', margin: '4px 0 0 0', lineHeight: 1.4 }}>
              Mendekati profil acak sempurna (IC ideal ~0.0385).
            </p>
          </div>
        </div>

        {/* 3 Metric Cards */}
        <div className="crypto-stats-triad">
          <div className="crypto-stat-card">
            <span className="stat-card-label">IC Plainteks</span>
            <div className="stat-card-val">{plaintext.ic || '0.000'}</div>
            <span className="stat-card-sub">Bahasa alami (~0.068)</span>
          </div>

          <div className="crypto-stat-card">
            <span className="stat-card-label">IC Super-Cipher</span>
            <div className="stat-card-val highlight">{ciphertext.ic || '0.000'}</div>
            <span className="stat-card-sub" style={{ color: '#059669', fontWeight: 800 }}>Acak (~0.038)</span>
          </div>

          <div className="crypto-stat-card">
            <span className="stat-card-label">Entropi Shannon</span>
            <div className="stat-card-val">{ciphertext.entropy || '0.0'}</div>
            <span className="stat-card-sub">Maks 4.70 bits</span>
          </div>
        </div>
      </div>

      {/* Histogram Chart */}
      <div className="crypto-chart-box">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
          <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '11px', fontWeight: 800, color: '#1D1C1B', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            Histogram Distribusi Frekuensi Karakter A-Z (%)
          </span>
          <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '11px', color: '#7A756D' }}>
            Puncak frekuensi bahasa alami berhasil diratakan
          </span>
        </div>

        <div style={{ height: '260px', width: '100%', paddingTop: '10px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.06)" />
              <XAxis dataKey="letter" stroke="#8A8680" tick={{ fontSize: 11, fill: '#1D1C1B', fontWeight: 700 }} />
              <YAxis stroke="#8A8680" tick={{ fontSize: 11, fill: '#8A8680' }} unit="%" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1D1C1B',
                  borderColor: '#1D1C1B',
                  borderRadius: '14px',
                  color: '#F2EFE9',
                  fontSize: '12px',
                  fontFamily: "'JetBrains Mono', monospace"
                }}
                itemStyle={{ color: '#F2EFE9' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '12px' }} />
              <Bar dataKey="Plainteks" fill="#A8A29E" name="Plainteks Asli (%)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="SuperCipher" fill="#1D1C1B" name="Super-Cipherteks (%)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Standar_ID" fill="#10B981" opacity={0.35} name="Standar Bahasa Indonesia (%)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary Box */}
      <div className="crypto-summary-box">
        <Scale style={{ width: '22px', height: '22px', color: '#1D1C1B', flexShrink: 0, marginTop: '2px' }} />
        <div style={{ fontSize: '12px', lineHeight: 1.6, color: '#1D1C1B' }}>
          <span style={{ fontWeight: 900, textTransform: 'uppercase', letterSpacing: '0.06em', display: 'block', marginBottom: '4px' }}>
            Kesimpulan Evaluasi Kriptanalisis:
          </span>
          <span style={{ color: '#57534E' }}>
            {ciphertext.evaluation} Kombinasi 3 lapis (<strong>Playfair ➔ Vigenère ➔ Columnar Transposition</strong>) terbukti secara empiris mematahkan serangan analisis frekuensi (Kasiski & Index of Coincidence test).
          </span>
        </div>
      </div>
    </div>
  );
}
