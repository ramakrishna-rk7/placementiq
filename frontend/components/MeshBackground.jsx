'use client';
import { useEffect, useRef } from 'react';

export default function MeshBackground() {
  const ref = useRef(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = 400;
    };
    resize();
    window.addEventListener('resize', resize);

    let t = 0;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const cols = 8;
      const rows = 4;
      const w = canvas.width / cols;
      const h = canvas.height / rows;
      for (let i = 0; i <= cols; i++) {
        for (let j = 0; j <= rows; j++) {
          const x = i * w + Math.sin(t / 20 + i) * 8;
          const y = j * h + Math.cos(t / 25 + j) * 8;
          const g = ctx.createRadialGradient(x, y, 0, x, y, 120);
          g.addColorStop(0, 'rgba(99,102,241,0.18)');
          g.addColorStop(0.5, 'rgba(139,92,246,0.12)');
          g.addColorStop(1, 'rgba(6,182,212,0.0)');
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(x, y, 120, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      t += 1;
      requestAnimationFrame(draw);
    };
    draw();

    return () => window.removeEventListener('resize', resize);
  }, []);

  return <canvas ref={ref} className="absolute inset-0 w-full h-[400px] opacity-60" />;
}
