# frontend/src/components/ChatPanel.jsx
import React, { useState } from "react";

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    { from: "ai", text: "Üdv! Én vagyok az MZ/X kereskedő AI. Miben segíthetek?" }
  ]);

  const [input, setInput] = useState("");

  const sendMsg = () => {
    if (!input.trim()) return;

    const userMsg = { from: "user", text: input };
    const aiMsg = { from: "ai", text: "(AI válasz – később WS-ből jön)" };

    setMessages(m => [...m, userMsg, aiMsg]);
    setInput("");
  };

  return (
    <div className="fixed bottom-0 left-0 w-full bg-black/70 border-t border-cyan-500/30 p-3 backdrop-blur-xl z-50">
      <div className="h-40 overflow-y-auto mb-3 bg-black/30 p-3 rounded-xl border border-cyan-500/20">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`my-1 p-2 rounded-lg max-w-[70%] ${
              m.from === "user"
                ? "ml-auto bg-cyan-600 text-black"
                : "mr-auto bg-green-600/40 border border-green-400/40"
            }`}
          >
            {m.text}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Írj üzenetet az AI-nak…"
          className="flex-1 bg-black border border-cyan-500/40 p-2 rounded text-green-300"
        />
        <button
          onClick={sendMsg}
          className="bg-cyan-600 hover:bg-cyan-500 text-black font-bold px-4 rounded-xl"
        >
          Küldés
        </button>
      </div>
    </div>
  );
}