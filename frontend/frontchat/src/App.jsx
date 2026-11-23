import { useState, useRef, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import KontenUtama from "./components/KontenUtama";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

const BASE_URL = "http://localhost:8000";

export default function App() {
  const [topikList, setTopikList]   = useState([]);
  const [kontenMap, setKontenMap]   = useState({});
  const [topikAktif, setTopikAktif] = useState(null);
  const [loading, setLoading]       = useState(true);
  const [chatOpen, setChatOpen]     = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const chatRef = useRef(null);

  // Fetch konten dari backend saat pertama load
  useEffect(() => {
    fetch(`${BASE_URL}/konten`)
      .then((r) => r.json())
      .then((data) => {
        // Buat map id → objek konten untuk lookup cepat
        const map = {};
        data.forEach((item) => { map[item.id] = item; });
        setTopikList(data);
        setKontenMap(map);
        setTopikAktif(data[0]?.id ?? null);
        setLoading(false);
      })
      .catch(() => {
        // Fallback kalau backend belum jalan
        setTopikList([]);
        setLoading(false);
      });
  }, []);

  function handleTanya(pertanyaan) {
    setChatOpen(true);
    setSidebarOpen(false);
    setTimeout(() => chatRef.current?.kirimDariLuar(pertanyaan), 100);
  }

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner" />
        <p>Memuat konten...</p>
      </div>
    );
  }

  if (topikList.length === 0) {
    return (
      <div className="loading-screen error">
        <p>⚠️ Tidak dapat terhubung ke server.</p>
        <p>Pastikan backend berjalan di <code>http://localhost:8000</code></p>
      </div>
    );
  }

  return (
    <div className="app-layout">

      {sidebarOpen && (
        <div className="overlay" onClick={() => setSidebarOpen(false)} />
      )}

      {/* ── Sidebar kiri ── */}
      <div className={`sidebar-wrapper ${sidebarOpen ? "open" : ""}`}>
        <Sidebar
          topikList={topikList}
          aktif={topikAktif}
          onPilih={(id) => { setTopikAktif(id); setSidebarOpen(false); }}
        />
      </div>

      {/* ── Konten tengah ── */}
      <div className="main-wrapper">
        <div className="mobile-topbar">
          <button className="hamburger" onClick={() => setSidebarOpen(true)}>☰</button>
          <span className="mobile-title">🏛️ Bantuan ATR/BPN</span>
        </div>

        <KontenUtama konten={kontenMap[topikAktif]} />
      </div>

      {/* ── FAB Chatbot ── */}
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
