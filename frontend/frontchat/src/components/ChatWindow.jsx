import { useState, useRef, useEffect, forwardRef, useImperativeHandle } from "react";
import { cariJawaban } from "../utils/chatEngine";
import { KATEGORI_LIST } from "../data/faqData";

function TypingDots() {
  return (
    <div className="typing-dots">
      <span /><span /><span />
    </div>
  );
}

function BubbleBot({ msg, onRekomendasi }) {
  if (msg.type === "typing") return (
    <div className="bubble-row bot">
      <div className="avatar bot-avatar">🤖</div>
      <div className="bubble bot-bubble"><TypingDots /></div>
    </div>
  );

  const { hasil } = msg;

  return (
    <div className="bubble-row bot">
      <div className="avatar bot-avatar">🤖</div>
      <div className="bubble bot-bubble">
        {hasil.status === "berhasil" ? (
          <>
            <p className="bubble-answer">{hasil.jawaban}</p>
            <div className="bubble-meta">
              <span className="badge">{hasil.kategori}</span>
              <span className="similarity">relevansi {hasil.similarity}</span>
            </div>
          </>
        ) : hasil.status === "tidak_ditemukan" ? (
          <>
            <p className="bubble-answer not-found">{hasil.pesan}</p>
            {hasil.rekomendasi?.length > 0 && (
              <div className="rekomendasi">
                <p className="rek-title">Mungkin maksud Anda:</p>
                {hasil.rekomendasi.map((r, i) => (
                  <button key={i} className="rek-item" onClick={() => onRekomendasi(r)}>
                    {r}
                  </button>
                ))}
              </div>
            )}
          </>
        ) : hasil.status === "error" ? (
          <p className="bubble-answer not-found">⚠️ {hasil.pesan}</p>
        ) : (
          <p className="bubble-answer not-found">{hasil.pesan}</p>
        )}
      </div>
    </div>
  );
}

function BubbleUser({ text }) {
  return (
    <div className="bubble-row user">
      <div className="bubble user-bubble">{text}</div>
      <div className="avatar user-avatar">👤</div>
    </div>
  );
}

export default forwardRef(function ChatWindow({ kategoriFilter, onClose }, ref) {
  const [messages, setMessages] = useState([
    {
      id: 0,
      from: "bot",
      type: "welcome",
      hasil: {
        status: "berhasil",
        jawaban:
          "Halo! Saya BPN-Bot, asisten virtual FAQ Portal PPAT ATR/BPN. Silakan tanyakan seputar akun SSO, pembuatan akta, peralihan hak, Hak Tanggungan, KJKSB, KKPR, atau kendala teknis portal.",
        kategori: "Selamat Datang",
        similarity: "—",
      },
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  const kategoriLabel =
    KATEGORI_LIST.find((k) => k.id === kategoriFilter)?.label || "Semua Topik";

  // Expose kirimDariLuar ke parent (App.jsx) via ref
  useImperativeHandle(ref, () => ({
    kirimDariLuar: (teks) => kirim(teks),
  }));

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function kirim(teks) {
    const q = teks || input.trim();
    if (!q || loading) return;
    setInput("");

    const userMsg = { id: Date.now(), from: "user", text: q };
    const typingMsg = { id: Date.now() + 1, from: "bot", type: "typing" };

    setMessages((prev) => [...prev, userMsg, typingMsg]);
    setLoading(true);

    try {
      const hasil = await cariJawaban(q, kategoriFilter);
      const botMsg = { id: Date.now() + 2, from: "bot", type: "answer", hasil };
      setMessages((prev) => [...prev.filter((m) => m.type !== "typing"), botMsg]);
    } catch {
      const botMsg = {
        id: Date.now() + 2,
        from: "bot",
        type: "answer",
        hasil: { status: "error", pesan: "Terjadi kesalahan. Pastikan backend berjalan di port 8000." },
      };
      setMessages((prev) => [...prev.filter((m) => m.type !== "typing"), botMsg]);
    } finally {
      setLoading(false);
    }
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      kirim();
    }
  }

  return (
    <div className="chat-window">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-header-left">
          <span className="chat-header-avatar">🤖</span>
          <div>
            <div className="chat-header-name">BPN-Bot</div>
            <div className="chat-header-status">
              <span className="online-dot" /> Online · {kategoriLabel}
            </div>
          </div>
        </div>
        <div className="chat-header-right">
          <span className="header-badge">FAQ PPAT</span>
          {onClose && (
            <button className="chat-close-btn" onClick={onClose} title="Tutup">✕</button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((msg) =>
          msg.from === "user" ? (
            <BubbleUser key={msg.id} text={msg.text} />
          ) : (
            <BubbleBot key={msg.id} msg={msg} onRekomendasi={(r) => kirim(r)} />
          )
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick questions */}
      <div className="quick-questions">
        {[
          "Akun PPAT tidak bisa login?",
          "Kode billing tidak muncul?",
          "Cara daftar Hak Tanggungan?",
          "Apa itu KJKSB?",
        ].map((q) => (
          <button key={q} className="quick-btn" onClick={() => kirim(q)}>
            {q}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="chat-input-area">
        <input
          className="chat-input"
          type="text"
          placeholder="Tulis pertanyaan seputar portal PPAT ATR/BPN..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading}
        />
        <button
          className="send-btn"
          onClick={() => kirim()}
          disabled={loading || !input.trim()}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
});
