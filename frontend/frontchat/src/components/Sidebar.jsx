import { useState } from "react";
import { KATEGORI_LIST, FAQ_DATA } from "../data/faqData";

export default function Sidebar({ aktif, onPilih, onTanya }) {
  const [expanded, setExpanded] = useState("semua");

  function toggleKategori(id) {
    // Klik kategori: set aktif filter + toggle accordion
    onPilih(id);
    setExpanded((prev) => (prev === id ? null : id));
  }

  // Ambil pertanyaan per kategori dari FAQ_DATA
  function getPertanyaan(kategoriId) {
    if (kategoriId === "semua") return [];
    return FAQ_DATA.filter((f) => f.kategori === kategoriId);
  }

  return (
    <aside className="sidebar">
      {/* ── Header ── */}
      <div className="sidebar-header">
        <span className="sidebar-logo">🏛️</span>
        <div>
          <div className="sidebar-title">Bantuan ATR/BPN</div>
          <div className="sidebar-sub">Portal Mitra PPAT</div>
        </div>
      </div>

      {/* ── Nav ── */}
      <nav className="sidebar-nav">
        {KATEGORI_LIST.map((kat) => {
          const pertanyaan = getPertanyaan(kat.id);
          const isExpanded = expanded === kat.id;
          const isAktif = aktif === kat.id;

          return (
            <div key={kat.id} className="sidebar-group">
              {/* Kategori item */}
              <button
                className={`sidebar-item ${isAktif ? "aktif" : ""}`}
                onClick={() => toggleKategori(kat.id)}
              >
                <span className="sidebar-icon">{kat.icon}</span>
                <span className="sidebar-label">{kat.label}</span>
                {pertanyaan.length > 0 && (
                  <span className={`sidebar-chevron ${isExpanded ? "open" : ""}`}>
                    ›
                  </span>
                )}
              </button>

              {/* Sub-items: daftar pertanyaan */}
              {pertanyaan.length > 0 && isExpanded && (
                <div className="sidebar-subitems">
                  {pertanyaan.map((faq) => (
                    <button
                      key={faq.id}
                      className="sidebar-subitem"
                      onClick={() => onTanya(faq.pertanyaan)}
                      title={faq.pertanyaan}
                    >
                      <span className="subitem-dot">•</span>
                      <span className="subitem-text">{faq.pertanyaan}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* ── Footer ── */}
      <div className="sidebar-footer">
        <div className="sidebar-footer-title">Butuh bantuan lain?</div>
        <a href="mailto:helpdesk@atrbpn.go.id" className="sidebar-link">
          📧 helpdesk@atrbpn.go.id
        </a>
        <a
          href="https://bantuan.atrbpn.go.id"
          target="_blank"
          rel="noreferrer"
          className="sidebar-link"
        >
          🌐 bantuan.atrbpn.go.id
        </a>
      </div>
    </aside>
  );
}
