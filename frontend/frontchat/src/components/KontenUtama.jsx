export default function KontenUtama({ konten }) {
  if (!konten) return (
    <main className="konten-utama">
      <p style={{ color: "#9ca3af", padding: "40px" }}>Pilih topik di sidebar.</p>
    </main>
  );

  return (
    <main className="konten-utama">
      <div className="konten-hero">
        <div className="konten-hero-icon">{konten.icon}</div>
        <div>
          <h1 className="konten-judul">{konten.judul}</h1>
          <p className="konten-subjudul">{konten.subjudul}</p>
        </div>
      </div>

      <div className="konten-divider" />

      <div className="konten-seksi-list">
        {konten.seksi?.map((seksi, idx) => (
          <section key={idx} className="konten-seksi">
            <h2 className="seksi-judul">
              <span className="seksi-nomor">{idx + 1}</span>
              {seksi.judul}
            </h2>
            <div className="seksi-isi">
              {seksi.isi.split("\n").map((baris, i) =>
                baris.trim() === "" ? null : (
                  <p key={i} className={
                    baris.startsWith("•") || baris.match(/^\d+\./) ? "seksi-poin" : ""
                  }>
                    {baris}
                  </p>
                )
              )}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
