import { KATEGORI_LIST } from "../data/faqData";

export default function Sidebar({ aktif, onPilih }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="sidebar-logo">🏛️</span>
        <div>
          <div className="sidebar-title">Bantuan ATR/BPN</div>
          <div className="sidebar-sub">Portal Mitra PPAT</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {KATEGORI_LIST.map((kat) => (
          <button
            key={kat.id}
            className={`sidebar-item ${aktif === kat.id ? "aktif" : ""}`}
            onClick={() => onPilih(kat.id)}
          >
            <span className="sidebar-icon">{kat.icon}</span>
            <span className="sidebar-label">{kat.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-title">Butuh bantuan lain?</div>
        <a href="mailto:helpdesk@atrbpn.go.id" className="sidebar-link">
          📧 helpdesk@atrbpn.go.id
        </a>
        <a href="https://bantuan.atrbpn.go.id" target="_blank" rel="noreferrer" className="sidebar-link">
          🌐 bantuan.atrbpn.go.id
        </a>
      </div>
    </aside>
  );
}
