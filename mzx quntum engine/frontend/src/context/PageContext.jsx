# frontend/src/context/PageContext.jsx
import { createContext, useContext, useState } from "react";

const PageContext = createContext();

export function PageProvider({ children }) {
  const [page, setPage] = useState("dashboard");

  const changePage = (p) => setPage(p);

  return (
    <PageContext.Provider value={{ page, changePage }}>
      {children}
    </PageContext.Provider>
  );
}

export function usePage() {
  return useContext(PageContext);
}

# UPDATED App.jsx WITH PageProvider
import React from 'react'
import { PageProvider } from './context/PageContext'
import Layout from './src/components/Layout'

export default function App(){
  return (
    <PageProvider>
      <Layout />
    </PageProvider>
  )
}

# UPDATED Layout.jsx USING usePage()
import React from "react";
import Dashboard from "./Dashboard";
import Modules from "./Modules";
import Position from "./Position";
import Settings from "./Settings";
import ChatPanel from "./ChatPanel";
import { usePage } from "../context/PageContext";

export default function Layout() {
  const { page, changePage } = usePage();

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
    <div className="w-full h-full relative">

      {/* TOP MENU */}
      <div className="fixed top-0 left-0 w-full bg-black/50 p-4 flex gap-6 text-cyan-300 border-b border-cyan-500/30 z-40 topnav">
        <button onClick={() => changePage("dashboard")} className="hover:text-white">Dashboard</button>
        <button onClick={() => changePage("modules")} className="hover:text-white">Modulok</button>
        <button onClick={() => changePage("position")} className="hover:text-white">Pozíció</button>
        <button onClick={() => changePage("settings")} className="hover:text-white">Beállítások</button>
      </div>

      {/* PAGE CONTENT */}
      <div className="pt-20 pb-40 p-4">
        {renderPage()}
      </div>

      {/* CHAT PANEL */}
      <ChatPanel />
    </div>
  );
}