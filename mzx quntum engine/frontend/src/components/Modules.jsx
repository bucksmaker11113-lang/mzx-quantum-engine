# frontend/src/components/Modules.jsx
import React from "react";

export default function Modules() {
  const modules = [
    { name: "SMC Engine", status: "Aktív", color: "purple" },
    { name: "Monte Carlo", status: "Aktív", color: "blue" },
    { name: "Regime Detector", status: "Range", color: "cyan" },
    { name: "Microstructure", status: "Stabil", color: "green" },
    { name: "Spread Detector", status: "Normál", color: "yellow" },
    { name: "Liquidity Map", status: "Magas", color: "cyan" },
    { name: "HFT Detector", status: "Nincs Spike", color: "orange" },
    { name: "Sequencer", status: "Optimalizált", color: "green" },
    { name: "Hybrid Bias", status: "Neutral", color: "purple" },
    { name: "Confidence Model", status: "0.64", color: "blue" },
    { name: "Arbitrage Engine", status: "Nincs eltérés", color: "cyan" },
    { name: "Auto Stop Engine", status: "Normál SL", color: "yellow" }
  ];

  return (
    <div className="w-full h-full flex flex-col gap-6 p-4 text-green-300">
      <div className="text-3xl font-bold text-cyan-300 tracking-wider mb-4">AI Modul Állapotok</div>
      <div className="grid grid-cols-2 gap-4">
        {modules.map((m, i) => (
          <div key={i} className={`p-4 rounded-xl bg-black/40 border border-${m.color}-500/40 shadow-lg`}>
            <div className="text-xl mb-1">{m.name}</div>
            <div className="text-sm opacity-80">Státusz: {m.status}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
