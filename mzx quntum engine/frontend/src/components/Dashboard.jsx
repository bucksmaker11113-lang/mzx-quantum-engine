
# frontend/src/components/Dashboard.jsx
import React, { useState, useEffect } from "react";

export default function Dashboard() {
  const [events, setEvents] = useState([
    "AI rendszer inicializálva…",
    "Pipeline betöltve…",
    "Várakozás piaci adatokra…"
  ]);

  const [pulse, setPulse] = useState(false);

  useEffect(() => {
    const i = setInterval(() => setPulse(p => !p), 1200);
    return () => clearInterval(i);
  }, []);

  return (
    <div className="w-full h-full flex flex-col gap-6 p-4">
      {/* BACKGROUND */}
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_center,rgba(0,255,180,0.12),transparent_70%)]"></div>

      <div className="text-3xl font-bold text-cyan-300 tracking-wider">
        MZ/X AI TRADER – DASHBOARD
      </div>

      {/* PRICE CARDS */}
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-black/50 border border-cyan-500/40 rounded-xl p-4 shadow-xl">
          <div className="text-xl text-cyan-300 mb-2">ETH/USDC – Live</div>
          <div className="text-4xl font-bold text-green-400">1700.00</div>
        </div>
        <div className="bg-black/50 border border-purple-500/40 rounded-xl p-4 shadow-xl">
          <div className="text-xl text-purple-300 mb-2">BTC/USDC – Live</div>
          <div className="text-4xl font-bold text-green-400">42000.00</div>
        </div>
      </div>

      {/* MARKET STATUS */}
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-black/40 border border-green-500/40 rounded-xl p-4">
          <div className="text-lg text-green-300">Bias</div>
          <div className="text-2xl font-bold text-green-400">NEUTRAL</div>
        </div>
        <div className="bg-black/40 border border-blue-500/40 rounded-xl p-4">
          <div className="text-lg text-blue-300">Trend</div>
          <div className="text-2xl font-bold text-blue-400">Range</div>
        </div>
        <div className="bg-black/40 border border-yellow-500/40 rounded-xl p-4">
          <div className="text-lg text-yellow-300">Volatility</div>
          <div className="text-2xl font-bold text-yellow-400">Low</div>
        </div>
      </div>

      {/* PULSE + EVENTS */}
      <div className="grid grid-cols-2 gap-6">
        <div className="flex flex-col items-center justify-center bg-black/40 border border-cyan-500/30 p-6 rounded-xl">
          <div className={`w-40 h-40 rounded-full bg-gradient-to-br from-cyan-400 to-purple-600 opacity-80 shadow-2xl transition-all duration-700 ${pulse ? 'scale-110 shadow-cyan-500/50' : 'scale-90 shadow-purple-500/40'}`}></div>
          <div className="mt-4 text-cyan-300 text-lg opacity-80 tracking-wide">Piaci impulzus aktivitás</div>
        </div>

        <div className="bg-black/40 border border-green-500/30 p-4 rounded-xl h-48 overflow-y-auto shadow-inner">
          <div className="text-green-300 text-lg mb-2">AI Event Feed</div>
          <div className="flex flex-col gap-2 text-sm">
            {events.map((e, i) => (
              <div key={i} className="p-2 bg-black/30 border border-green-500/20 rounded-lg">{e}</div>
            ))}
          </div>
        </div>
      </div>

      {/* SMC + MC */}
      <div className="grid grid-cols-2 gap-6 mt-4">
        <div className="bg-black/40 p-4 rounded-xl border border-purple-500/30">
          <div className="text-purple-300 text-xl mb-3">SMC Jelzések</div>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="p-2 bg-black/30 border border-purple-500/30 rounded">BOS: nincs</div>
            <div className="p-2 bg-black/30 border border-purple-500/30 rounded">CHoCH: nincs</div>
            <div className="p-2 bg-black/30 border border-purple-500/30 rounded">FVG UP: nincs</div>
            <div className="p-2 bg-black/30 border border-purple-500/30 rounded">FVG DOWN: nincs</div>
            <div className="p-2 bg-black/30 border border-purple-500/30 rounded">Sweep: nincs</div>
            <div className="p-2 bg-black/30 border border-purple-500/30 rounded">Displacement: nincs</div>
          </div>
        </div>

        <div className="bg-black/40 p-4 rounded-xl border border-blue-500/30">
          <div className="text-blue-300 text-xl mb-3">Monte Carlo</div>
          <div className="flex flex-col gap-2 text-sm">
            <div className="p-2 bg-black/30 border border-blue-500/30 rounded">Trend Probability: 50%</div>
            <div className="p-2 bg-black/30 border border-blue-500/30 rounded">Reversal Probability: 50%</div>
            <div className="p-2 bg-black/30 border border-blue-500/30 rounded">Volatility Score: 0.02</div>
          </div>
        </div>
      </div>

      {/* MODULE STATUS */}
      <div className="bg-black/40 mt-4 p-4 rounded-xl border border-cyan-500/40">
        <div className="text-cyan-300 text-xl mb-3">AI Modul Állapotok</div>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="p-2 bg-black/30 border border-cyan-500/30 rounded">Confidence Model: OK</div>
          <div className="p-2 bg-black/30 border border-cyan-500/30 rounded">HFT Detector: nincs spike</div>
          <div className="p-2 bg-black/30 border border-cyan-500/30 rounded">Spread Detector: normál</div>
          <div className="p-2 bg-black/30 border border-cyan-500/30 rounded">Liquidity Map: stabil</div>
          <div className="p-2 bg-black/30 border border-cyan-500/30 rounded">Hybrid Bias: neutral</div>
          <div className="p-2 bg-black/30 border border-cyan-500/30 rounded">Regime: range</div>
        </div>
      </div>
    </div>
  );
}