// src/components/BackgroundDivider.jsx
import React from 'react';

function BackgroundDivider() {
  return (
    <div className="fixed top-0 left-0 w-full h-full bg-slate-950 overflow-hidden z-0">
      {/* First Radial Gradient Circle */}
      <div className="absolute bottom-0 left-[-20%] top-[-10%] h-[500px] w-[500px] rounded-full bg-[radial-gradient(circle_farthest-side,rgba(255,0,182,0.15),rgba(255,255,255,0))] animate-pulseSlow"></div>
      
      {/* Second Radial Gradient Circle */}
      <div className="absolute bottom-0 right-[-20%] top-[-10%] h-[500px] w-[500px] rounded-full bg-[radial-gradient(circle_farthest-side,rgba(255,0,182,0.15),rgba(255,255,255,0))] animate-pulseSlow delay-2s"></div>
    </div>
  );
}

export default BackgroundDivider;