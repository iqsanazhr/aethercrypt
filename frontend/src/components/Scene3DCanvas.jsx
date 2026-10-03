import React, { Suspense, useRef, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { useGLTF, Float, Center, Environment, OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import gsap from 'gsap';

// Model Cryptex
function CryptexModel({ isSpinning = false }) {
  const { scene } = useGLTF('/models/da_vinci_code_cryptex.glb');
  const ref = useRef();

  useFrame((_, delta) => {
    if (ref.current) {
      ref.current.rotation.y += delta * (isSpinning ? 4.5 : 0.4);
    }
  });

  return (
    <primitive 
      ref={ref} 
      object={scene} 
      scale={0.019} // Skala pas, di tengah layar
      position={[0, 0, 0]}
    />
  );
}

// Model Enigma Machine
function EnigmaModel({ currentScene = 1, isSpinning = false }) {
  const { scene } = useGLTF('/models/enigma_machine_1934.glb');
  const ref = useRef();

  // Matikan lampu bawaan Blender (point light 54.000+ lumen) yang bikin model silau/terbakar
  useEffect(() => {
    if (scene) {
      scene.traverse((obj) => {
        if (obj.isLight) {
          obj.visible = false;
        }
      });
    }
  }, [scene]);

  // Transisi rotasi model per scene agar di Tahap 3 (Plugboard) model lurus sempurna
  useEffect(() => {
    if (!ref.current) return;

    let targetRot = [0.2, -0.25, 0];
    if (currentScene === 2) {
      targetRot = [0.25, -0.32, 0];
    } else if (currentScene === 3) {
      targetRot = [0.10, 0, 0]; // Lurus 100% tegak dan simetris (Y = 0, Z = 0)
    }

    const tween = gsap.to(ref.current.rotation, {
      x: targetRot[0],
      y: targetRot[1],
      z: targetRot[2],
      duration: 1.6,
      ease: 'power3.inOut',
    });

    return () => tween.kill();
  }, [currentScene]);

  useFrame((_, delta) => {
    if (ref.current) {
      if (isSpinning) {
        ref.current.rotation.y += delta * 2.5;
      }
    }
  });

  return (
    <primitive 
      ref={ref} 
      object={scene} 
      scale={0.10} // Zoom out lebih jauh lagi agar seluruh Enigma dan penutup kayunya tampil proporsional
      position={[0, -0.2, 0]}
      rotation={[0.2, -0.25, 0]}
    />
  );
}

// Model Mechanical Puzzle Box
function PuzzleBoxModel({ isSpinning = false }) {
  const { scene } = useGLTF('/models/puzzle_box_01.glb');
  const ref = useRef();

  useEffect(() => {
    if (scene) {
      // Pusatkan geometri objek tepat ke titik origin (0, 0, 0) agar simetris vertikal dan horizontal
      const box = new THREE.Box3().setFromObject(scene);
      const center = new THREE.Vector3();
      box.getCenter(center);
      scene.position.sub(center);
    }
  }, [scene]);

  useFrame((_, delta) => {
    if (ref.current) {
      ref.current.rotation.y += delta * (isSpinning ? 3.5 : 0.35);
      ref.current.rotation.x = Math.sin(Date.now() * 0.001) * 0.06;
    }
  });

  return (
    <primitive 
      ref={ref} 
      object={scene} 
      scale={7.5} // Ukuran pas, proporsional, tidak terlalu zoom in dan jelas
      position={[0, 0, 0]}
    />
  );
}

// Camera Controller dynamically transitions camera position based on currentScene
function CameraController({ currentScene, controlsRef }) {
  const { camera } = useThree();

  useEffect(() => {
    // Konfigurasi waypoint kamera untuk setiap scene
    const sceneCameraConfigs = [
      // Scene 0: Cryptex Centerpiece (Tepat di Tengah Layar - Zoom Out Utuh)
      { pos: [0, 0.2, 10.5], target: [0, 0, 0] },
      
      // Scene 1: Enigma Machine (Anotasi 1: Keyboard Input - kamera saat ini tanpa node)
      { pos: [0, 1.8, 14.5], target: [0, -0.4, 0] },
      
      // Scene 2: Enigma Machine (Node 'Camera' dari Blender - Sudut Atas-Kanan)
      { pos: [1.25, 0.78, 4.41], target: [-0.69, -1.13, 0.21] },
      
      // Scene 3: Enigma Machine (Plugboard Steckerbrett - Lurus Sempurna di Tengah Layar)
      { pos: [0, 0.6, 13.6], target: [0, -0.6, 0] },
      
      // Scene 4: Mechanical Puzzle Box (Pas di Tengah Sumbu Vertikal & Horizontal)
      { pos: [0, 0, 6.2], target: [0, 0, 0] },
    ];

    const config = sceneCameraConfigs[currentScene] || sceneCameraConfigs[0];
    
    // Animate camera position smoothly using GSAP
    const posTween = gsap.to(camera.position, {
      x: config.pos[0],
      y: config.pos[1],
      z: config.pos[2],
      duration: 1.8,
      ease: 'power3.inOut',
    });

    const targetLookAt = new THREE.Vector3(...config.target);
    const proxy = { t: 0 };

    const lookTween = gsap.to(proxy, {
      t: 1,
      duration: 1.8,
      ease: 'power3.inOut',
      onUpdate: () => {
        if (controlsRef?.current) {
          controlsRef.current.target.lerp(targetLookAt, 0.1);
          controlsRef.current.update();
        } else {
          camera.lookAt(targetLookAt);
        }
      }
    });

    return () => {
      posTween.kill();
      lookTween.kill();
    };
  }, [currentScene, camera, controlsRef]);

  return null;
}

export default function Scene3DCanvas({ currentScene = 0, isProcessing = false }) {
  const controlsRef = useRef();

  return (
    <div className="absolute inset-0 w-full h-full z-0 pointer-events-none">
      <Canvas 
        camera={{ position: [0, 0.2, 10.5], fov: 38 }}
        gl={{ 
          antialias: true, 
          alpha: true,
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: 1.0
        }}
      >
        <ambientLight intensity={0.45} />
        <directionalLight position={[10, 15, 10]} intensity={1.2} color="#ffffff" />
        <directionalLight position={[-10, 10, -10]} intensity={0.5} color="#e2ded7" />
        <pointLight position={[0, -2, 2]} intensity={0.2} color="#ffd494" />

        <Suspense fallback={null}>
          <CameraController currentScene={currentScene} controlsRef={controlsRef} />

          {/* Render Model berdasarkan Scene */}
          {currentScene === 0 && (
            <Float speed={1.5} rotationIntensity={0.2} floatIntensity={0.3}>
              <Center>
                <CryptexModel isSpinning={isProcessing} />
              </Center>
            </Float>
          )}

          {(currentScene === 1 || currentScene === 2 || currentScene === 3) && (
            <Float speed={1.2} rotationIntensity={0.1} floatIntensity={0.2}>
              <Center>
                <EnigmaModel currentScene={currentScene} isSpinning={isProcessing} />
              </Center>
            </Float>
          )}

          {currentScene === 4 && (
            <Float speed={1.2} rotationIntensity={0.15} floatIntensity={0.15}>
              <Center>
                <PuzzleBoxModel isSpinning={isProcessing} />
              </Center>
            </Float>
          )}

          <Environment preset="apartment" environmentIntensity={0.6} />
        </Suspense>

        <OrbitControls 
          ref={controlsRef}
          enableZoom={true} 
          enablePan={false} 
          maxDistance={16} 
          minDistance={0.4}
          maxPolarAngle={Math.PI / 2 + 0.2}
          minPolarAngle={Math.PI / 6}
        />
      </Canvas>
    </div>
  );
}
