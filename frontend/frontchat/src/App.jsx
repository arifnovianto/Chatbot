import { useState, useRef } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

export default function App() {
  const [kategoriAktif, setKategoriAktif] = useState("semua");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const chatRef = useRef(null);

  // Dipanggil sidebar saat user klik pertanyaan → langsung kirim ke chat
  function handleTanya(pertanyaan) {
    setSidebarOpen(false);
    chatRef.current?.kirimDariLuar(pertanyaan);
  }

  return (
    <div className="app-layout">
      {sidebarOpen && (
        <div className="overlay" onClick={() => setSidebarOpen(false)} />
      )}

      <div className={`sidebar-wrapper ${sidebarOpen ? "open" : ""}`}>
        <Sidebar
          aktif={kategoriAktif}
          onPilih={(id) => {
            setKategoriAktif(id);
          }}
          onTanya={handleTanya}
        />
      </div>

      <div className="main-wrapper">
        <div className="mobile-topbar">
          <button className="hamburger" onClick={() => setSidebarOpen(true)}>
            ☰
          </button>
          <span className="mobile-title">🏛️ FAQ Portal PPAT</span>
        </div>

        <ChatWindow
          ref={chatRef}
          kategoriFilter={kategoriAktif}
        />
      </div>
    </div>
  );
}
