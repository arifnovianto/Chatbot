import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

export default function App() {
  const [kategoriAktif, setKategoriAktif] = useState("semua");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-layout">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="overlay" onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <div className={`sidebar-wrapper ${sidebarOpen ? "open" : ""}`}>
        <Sidebar
          aktif={kategoriAktif}
          onPilih={(id) => {
            setKategoriAktif(id);
            setSidebarOpen(false);
          }}
        />
      </div>

      {/* Main */}
      <div className="main-wrapper">
        {/* Mobile topbar */}
        <div className="mobile-topbar">
          <button className="hamburger" onClick={() => setSidebarOpen(true)}>
            ☰
          </button>
          <span className="mobile-title">🏛️ FAQ Portal PPAT</span>
        </div>

        <ChatWindow kategoriFilter={kategoriAktif} />
      </div>
    </div>
  );
}
