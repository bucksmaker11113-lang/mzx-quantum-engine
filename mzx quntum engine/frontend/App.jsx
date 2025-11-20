# --------------------------------------
# FRONTEND ROOT – App.jsx (FINAL)
# --------------------------------------
import React, { useState } from "react";
import Layout from "./components/Layout";
import Dashboard from "./components/Dashboard";
import Modules from "./components/Modules";
import Position from "./components/Position";
import Settings from "./components/Settings";
import ChatPanel from "./components/ChatPanel";

export default function App() {
  const [page, setPage] = useState("dashboard");

  const renderPage = () => {
    switch (page) {
      case "dashboard": return <Dashboard />;
      case "modules": return <Modules />;
      case "position": return <Position />;
      case "settings": return <Settings />;
      default: return <Dashboard />;
    }
  };

  return (
    <Layout>

      {/* ------------------------------ */}
      {/* NAVIGATION BAR                */}
      {/* ------------------------------ */}
      <div className="w-full flex gap-4 mb-6 text-cyan-300 text-lg font-semibold">
        <button onClick={() => setPage("dashboard")} className="hover:text-green-300 transition">Dashboard</button>
        <button onClick={() => setPage("modules")} className="hover:text-green-300 transition">Modulok</button>
        <button onClick={() => setPage("position")} className="hover:text-green-300 transition">Pozíció</button>
        <button onClick={() => setPage("settings")} className="hover:text-green-300 transition">Beállítások</button>
      </div>

      {/* ------------------------------ */}
      {/* PAGE RENDER                    */}
      {/* ------------------------------ */}
      {renderPage()}

      {/* ------------------------------ */}
      {/* CHAT PANEL (always visible)    */}
      {/* ------------------------------ */}
      <ChatPanel />

    </Layout>
  );
}