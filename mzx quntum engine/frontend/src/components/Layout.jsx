 --------------------------------------
# src/components/Layout.jsx – FINAL FUTURISTIC LAYOUT
# --------------------------------------
import React from "react";
import Header from "./Header";

export default function Layout({ children }) {
  return (
    <div className="w-full h-full min-h-screen bg-black text-green-300 overflow-hidden relative">

      {/* --- BACKGROUND HOLOGRAPHIC GRID --- */}
      <div className="absolute inset-0 -z-10 opacity-40 bg-[radial-gradient(circle_at_center,rgba(0,255,200,0.12),transparent_70%)]"></div>

      <div className="absolute inset-0 -z-20 bg-[linear-gradient(90deg,rgba(0,255,255,0.05)_1px,transparent_1px),linear-gradient(0deg,rgba(0,255,255,0.05)_1px,transparent_1px)] bg-[size:40px_40px]"></div>

      {/* GLOW EFFECTS */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-cyan-500/20 blur-[130px] -z-30"></div>
      <div className="absolute bottom-0 right-1/2 translate-x-1/2 w-[600px] h-[300px] bg-purple-500/20 blur-[140px] -z-30"></div>

      {/* HEADER */}
      <Header />

      {/* MAIN CONTENT */}
      <div className="pt-4 pb-48 max-w-6xl mx-auto px-4">
        {children}
      </div>
    </div>
  );
}