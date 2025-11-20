# frontend/src/components/Position.jsx
import React from "react";

export default function Position() {
  const pos = {
    status: "Nincs aktív pozíció",
    direction: "FLAT",
    entry: null,
    mark: 1700.0,
    sl: null,
    tp: null,
    rr: null,
    pnl: 0
  };

  return (
    <div className="w-full h-full flex flex-col gap-6 p-4 text-green-300">
      <div className="text-3xl font-bold text-cyan-300 tracking-wider mb-4">Pozíció Kezelő Panel</div>

      <div className="bg-black/40 border border-cyan-500/40 rounded-xl p-6 shadow-xl">
        <div className="text-xl mb-2">Státusz</div>
        <div className="text-3xl font-bold text-green-400">{pos.status}</div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-black/40 border border-purple-500/40 rounded-xl p-4">
          <div className="text-lg">Irány</div>
          <div className="text-2xl font-bold text-purple-300">{pos.direction}</div>
        </div>

        <div className="bg-black/40 border border-yellow-500/40 rounded-xl p-4">
          <div className="text-lg">Aktuális ár</div>
          <div className="text-2xl font-bold text-yellow-300">{pos.mark}</div>
        </div>

        <div className="bg-black/40 border border-green-500/40 rounded-xl p-4">
          <div className="text-lg">Belépő ár</div>
          <div className="text-xl text-green-300">{pos.entry ?? "—"}</div>
        </div>

        <div className="bg-black/40 border border-red-500/40 rounded-xl p-4">
          <div className="text-lg">Stop Loss</div>
          <div className="text-xl text-red-300">{pos.sl ?? "—"}</div>
        </div>

        <div className="bg-black/40 border border-blue-500/40 rounded-xl p-4">
          <div className="text-lg">Take Profit</div>
          <div className="text-xl text-blue-300">{pos.tp ?? "—"}</div>
        </div>

        <div className="bg-black/40 border border-cyan-500/40 rounded-xl p-4">
          <div className="text-lg">RR mutató</div>
          <div className="text-xl text-cyan-300">{pos.rr ?? "—"}</div>
        </div>
      </div>

      <div className="bg-black/40 border border-green-500/40 rounded-xl p-6 shadow-xl mt-4">
        <div className="text-lg">Profit / Loss</div>
        <div className={`text-4xl font-bold ${pos.pnl >= 0 ? "text-green-400" : "text-red-400"}`}>{pos.pnl}</div>
      </div>
    </div>
  );
}
