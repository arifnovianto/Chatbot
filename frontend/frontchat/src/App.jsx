import { useState, useRef } from "react";
import Sidebar from "./components/Sidebar";
import KontenUtama from "./components/KontenUtama";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

export default function App() {
  const [topikAktif, setTopikAktif] = useState("beranda");
  const [chatOpen, setChatOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const chatRef = useRef(null);

  function handleTanya(pertanyaan) {
    setChatOpen(true);
    setTimeout(() => chatRef.current?.kirimDariLuar(pertanyaan), 100);
  }

  return (
    <div className="app-layout">

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="overlay" onClick={() => setSidebarOpen(false)} />
      )}

      {/* ── Sidebar kiri ── */}
      <div className={`sidebar-wrapper ${sidebarOpen ? "open" : ""}`}>
        <Sidebar
          aktif={topikAktif}
          onPilih={(id) => { setTopikAktif(id); setSidebarOpen(false); }}
        />
      </div>

      {/* ── Konten tengah ── */}
      <div className="main-wrapper">

        {/* Mobile topbar */}
        <div className="mobile-topbar">
          <button className="hamburger" onClick={() => setSidebarOpen(true)}>☰</button>
          <span className="mobile-title">🏛️ Bantuan ATR/BPN</span>
        </div>

        <KontenUtama topikId={topikAktif} />
      </div>

      {/* ── FAB Chatbot kanan bawah ── */}
      <button
        className={`fab-btn ${chatOpen ? "fab-open" : ""}`}
        onClick={() => setChatOpen((v) => !v)}
        title="Tanya BPN-Bot"
      >
        {chatOpen ? (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
          </svg>
        ) : (
          <>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span className="fab-label">BPN-Bot</span>
          </>
        )}
      </button>

      {/* ── Chat popup ── */}
      {chatOpen && (
        <div className="chat-popup">
          <ChatWindow
            ref={chatRef}
            kategoriFilter={null}
            onClose={() => setChatOpen(false)}
          />
        </div>
      )}

    </div>
  );
}
