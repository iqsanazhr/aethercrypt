import React, { Suspense, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, useGLTF, Float, Center, Environment, ContactShadows } from '@react-three/drei';
import { KeyRound, Sparkles, Layers } from 'lucide-react';

function Model({ url, scale = 1, isSpinning = false }) {
  const { scene } = useGLTF(url);
  const modelRef = useRef();

  useFrame((_, delta) => {
    if (modelRef.current) {
      if (isSpinning) {
        modelRef.current.rotation.y += delta * 4.5;
      } else {
        modelRef.current.rotation.y += delta * 0.4;
      }
    }
  });

  return (
    <primitive 
      ref={modelRef} 
      object={scene} 
      scale={scale} 
      dispose={null} 
    />
  );
}

function LoadingFallback() {
  const meshRef = useRef();
  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta;
      meshRef.current.rotation.y += delta * 1.5;
    }
  });

  return (
    <mesh ref={meshRef}>
      <torusKnotGeometry args={[1, 0.3, 100, 16]} />
      <meshStandardMaterial color="#1D1C1B" wireframe />
    </mesh>
  );
}

export default function ThreeViewer({ isEncrypting = false }) {
  const [activeModel, setActiveModel] = useState('cryptex');

  const models = {
    cryptex: {
      name: "Da Vinci Cryptex",
      url: "/models/da_vinci_code_cryptex.glb",
      scale: 0.09,
      desc: "Silinder Sandi Logam Kuningan A-Z (Representasi Vigenère & Caesar)",
      cameraPos: [0, 1.2, 4.2]
    },
    enigma: {
      name: "Enigma Machine 1934",
      url: "/models/enigma_machine_1934.glb",
      scale: 0.75,
      desc: "Mesin Sandi Rotor Bersejarah (Rotor & Papan Lampu)",
      cameraPos: [0, 3.2, 5.2]
    },
    puzzle_box: {
      name: "Mechanical Puzzle Box",
      url: "/models/puzzle_box_01.glb",
      scale: 1.3,
      desc: "Brankas Misteri Mekanikal (Indikator Kunci Validasi Dekripsi)",
      cameraPos: [0, 1.8, 3.8]
    }
  };

  const current = models[activeModel];

  return (
    <div className="three-viewer-card">
      
      {/* Background Ambient Glows */}
      <div className="ambient-glow-1 opacity-70"></div>
      <div className="ambient-glow-2 opacity-50"></div>

      {/* Top Header Control Bar with macOS Dots */}
      <div className="absolute top-6 left-6 right-6 z-20 flex flex-wrap items-center justify-between gap-4 pointer-events-auto">
        
        {/* macOS Window Controls */}
        <div className="flex items-center gap-2">
          <div className="w-3.5 h-3.5 rounded-full bg-[#ff5f56] shadow-sm"></div>
          <div className="w-3.5 h-3.5 rounded-full bg-[#ffbd2e] shadow-sm"></div>
          <div className="w-3.5 h-3.5 rounded-full bg-[#27c93f] shadow-sm"></div>
          <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-[var(--text-muted)] ml-2">
            ARTEFAK 3D MUSEUM •
          </span>
        </div>

        {/* Model Switcher Pills with explicit CSS classes */}
        <div className="model-pill-group">
          <button
            type="button"
            onClick={() => setActiveModel('cryptex')}
            className={`model-pill-btn ${activeModel === 'cryptex' ? 'active' : ''}`}
          >
            Cryptex
          </button>
          <button
            type="button"
            onClick={() => setActiveModel('enigma')}
            className={`model-pill-btn ${activeModel === 'enigma' ? 'active' : ''}`}
          >
            Enigma
          </button>
          <button
            type="button"
            onClick={() => setActiveModel('puzzle_box')}
            className={`model-pill-btn ${activeModel === 'puzzle_box' ? 'active' : ''}`}
          >
            Puzzle Box
          </button>
        </div>
      </div>

      {/* 3D Canvas */}
      <div className="flex-1 w-full h-full cursor-grab active:cursor-grabbing">
        <Canvas camera={{ position: current.cameraPos, fov: 45 }}>
          <ambientLight intensity={1.5} />
          <directionalLight position={[10, 15, 10]} intensity={2.0} color="#ffffff" />
          <directionalLight position={[-10, 10, -10]} intensity={1.0} color="#e0ded8" />
          <pointLight position={[0, -2, 0]} intensity={0.4} color="#ffd280" />

          <Suspense fallback={<LoadingFallback />}>
            <Float speed={1.8} rotationIntensity={0.25} floatIntensity={0.4}>
              <Center>
                <Model 
                  key={current.url} 
                  url={current.url} 
                  scale={current.scale} 
                  isSpinning={isEncrypting} 
                />
              </Center>
            </Float>
            <Environment preset="apartment" />
          </Suspense>

          <OrbitControls 
            enableZoom={true} 
            enablePan={false} 
            maxPolarAngle={Math.PI / 2 + 0.1} 
            minPolarAngle={Math.PI / 4} 
          />
        </Canvas>
      </div>

      {/* Bottom Floating Bar */}
      <div className="absolute bottom-5 left-6 right-6 z-20 flex flex-wrap items-center justify-between gap-3 text-xs bg-white/80 backdrop-blur-md py-3 px-5 rounded-2xl border border-white/90 shadow-sm pointer-events-auto">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-[var(--text-primary)] text-[var(--bg-primary)] flex items-center justify-center shadow-xs">
            <KeyRound className="w-3.5 h-3.5" />
          </div>
          <div>
            <span className="font-heading font-extrabold text-sm text-[var(--text-primary)] block leading-tight">
              {current.name}
            </span>
            <span className="text-[11px] text-[var(--text-muted)] font-mono leading-tight">
              {current.desc}
            </span>
          </div>
        </div>
        <div className="flex items-center text-[11px] font-mono text-[var(--text-muted)] bg-black/[0.04] px-3 py-1.5 rounded-full border border-black/[0.04]">
          <span>🖱️ Tahan & Geser untuk rotasi 360°</span>
        </div>
      </div>
    </div>
  );
}

useGLTF.preload('/models/da_vinci_code_cryptex.glb');
useGLTF.preload('/models/enigma_machine_1934.glb');
useGLTF.preload('/models/puzzle_box_01.glb');
