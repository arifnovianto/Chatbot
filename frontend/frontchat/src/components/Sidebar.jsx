export default function Sidebar({ topikList, aktif, onPilih }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-header-logo">🏛️</div>
        <div>
          <div className="sidebar-title">Bantuan ATR/BPN</div>
          <div className="sidebar-sub">Portal Mitra PPAT</div>
        </div>
      </div>

      <div className="sidebar-toc-title">Topik Panduan</div>
      <nav className="sidebar-nav">
        {topikList.map((item) => (
          <button
            key={item.id}
            className={`sidebar-item ${aktif === item.id ? "aktif" : ""}`}
            onClick={() => onPilih(item.id)}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-label">{item.label}</span>
            {aktif === item.id && <span className="sidebar-active-dot" />}
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
