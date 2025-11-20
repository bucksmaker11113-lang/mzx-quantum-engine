# frontend/src/components/Settings.jsx
import React, { useState } from "react";

export default function Settings() {
  const [mode, setMode] = useState("DEMO");
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [email, setEmail] = useState("");
  const [symbol, setSymbol] = useState("ETHUSDC");
  const [lev, setLev] = useState(5);

  const saveSettings = () => {
    alert("Beállítások mentve (mock)!");
  };

  return (
    <div className="w-full h-full flex flex-col gap-6 p-4 text-green-300">
      <div className="text-3xl font-bold text-cyan-300 tracking-wider mb-4">Rendszer Beállítások</div>

      <div className="bg-black/40 border border-cyan-500/40 rounded-xl p-4">
        <div className="text-xl mb-2">Üzemmód</div>
        <select value={mode} onChange={e => setMode(e.target.value)} className="bg-black border border-cyan-500/40 p-2 rounded w-full">
          <option value="DEMO">DEMO mód</option>
          <option value="LIVE">LIVE mód</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-black/40 border border-yellow-500/40 rounded-xl p-4">
          <div className="text-lg mb-1">API Key</div>
          <input value={apiKey} onChange={e => setApiKey(e.target.value)} className="w-full bg-black border border-yellow-500/40 p-2 rounded" />
        </div>

        <div className="bg-black/40 border border-red-500/40 rounded-xl p-4">
          <div className="text-lg mb-1">API Secret</div>
          <input value={apiSecret} onChange={e => setApiSecret(e.target.value)} className="w-full bg-black border border-red-500/40 p-2 rounded" />
        </div>
      </div>

      <div className="bg-black/40 border border-green-500/40 rounded-xl p-4">
        <div className="text-lg mb-1">Napi riport email</div>
        <input value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-black border border-green-500/40 p-2 rounded" />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-black/40 border border-purple-500/40 rounded-xl p-4">
          <div className="text-lg mb-1">Kereskedési pár</div>
          <select value={symbol} onChange={e => setSymbol(e.target.value)} className="w-full bg-black border border-purple-500/40 p-2 rounded">
            <option value="ETHUSDC">ETH/USDC</option>
            <option value="BTCUSDC">BTC/USDC</option>
          </select>
        </div>

        <div className="bg-black/40 border border-blue-500/40 rounded-xl p-4">
          <div className="text-lg mb-1">Tőkeáttétel</div>
          <input type="number" min="1" max="50" value={lev} onChange={e => setLev(e.target.value)} className="w-full bg-black border border-blue-500/40 p-2 rounded" />
        </div>
      </div>

      <button onClick={saveSettings} className="mt-4 bg-cyan-600 hover:bg-cyan-500 transition text-black font-bold p-3 rounded-xl shadow-xl">
        Beállítások mentése
      </button>
    </div>
  );