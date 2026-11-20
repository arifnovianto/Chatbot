// Mesin pencari jawaban berbasis TF-IDF sederhana (pure JS, no library)
import { FAQ_DATA } from "../data/faqData";

// ── Stopwords Bahasa Indonesia ──────────────────────────────────
const STOPWORDS = new Set([
  "yang","dan","di","ke","dari","ini","itu","ada","tidak","dengan","untuk",
  "pada","adalah","atau","juga","dalam","sudah","akan","bisa","saya","anda",
  "kita","mereka","kami","nya","ya","tidak","lagi","harus","dapat","bagaimana",
  "apa","mengapa","kenapa","kapan","berapa","siapa","apakah","cara","hal",
  "jika","bila","karena","sehingga","maka","tetapi","namun","tapi","lalu",
  "kemudian","setelah","sebelum","saat","ketika","oleh","hingga","sampai",
]);

// ── Preprocessing ───────────────────────────────────────────────
function preprocess(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 1 && !STOPWORDS.has(w));
}

// ── TF-IDF sederhana ────────────────────────────────────────────
function termFreq(tokens) {
  const tf = {};
  tokens.forEach((t) => (tf[t] = (tf[t] || 0) + 1));
  const len = tokens.length || 1;
  Object.keys(tf).forEach((k) => (tf[k] /= len));
  return tf;
}

// Pre-compute corpus tokens
const corpus = FAQ_DATA.map((item) => preprocess(item.pertanyaan + " " + item.jawaban));

// IDF
function buildIDF() {
  const N = corpus.length;
  const df = {};
  corpus.forEach((tokens) => {
    new Set(tokens).forEach((t) => (df[t] = (df[t] || 0) + 1));
  });
  const idf = {};
  Object.keys(df).forEach((t) => (idf[t] = Math.log((N + 1) / (df[t] + 1)) + 1));
  return idf;
}

const IDF = buildIDF();

function tfidfVector(tokens) {
  const tf = termFreq(tokens);
  const vec = {};
  Object.keys(tf).forEach((t) => (vec[t] = tf[t] * (IDF[t] || 1)));
  return vec;
}

function cosineSim(vecA, vecB) {
  const keysA = Object.keys(vecA);
  if (!keysA.length) return 0;
  let dot = 0;
  let normA = 0;
  let normB = 0;
  keysA.forEach((k) => {
    dot += vecA[k] * (vecB[k] || 0);
    normA += vecA[k] ** 2;
  });
  Object.values(vecB).forEach((v) => (normB += v ** 2));
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) || 1);
}

// ── Fungsi utama ─────────────────────────────────────────────────
export function cariJawaban(pertanyaan, filterKategori = null) {
  const queryTokens = preprocess(pertanyaan);
  if (!queryTokens.length) {
    return { status: "kosong", pesan: "Silakan ketik pertanyaan Anda." };
  }

  const queryVec = tfidfVector(queryTokens);

  // Hitung similarity ke semua data
  let candidates = FAQ_DATA.map((item, idx) => {
    const docVec = tfidfVector(corpus[idx]);
    return { item, score: cosineSim(queryVec, docVec) };
  });

  // Filter kategori jika ada
  if (filterKategori && filterKategori !== "semua") {
    candidates = candidates.filter((c) => c.item.kategori === filterKategori);
  }

  candidates.sort((a, b) => b.score - a.score);

  const best = candidates[0];

  if (!best || best.score < 0.08) {
    // Ambil 3 rekomendasi dari seluruh data (tanpa filter)
    const allSorted = FAQ_DATA.map((item, idx) => ({
      item,
      score: cosineSim(queryVec, tfidfVector(corpus[idx])),
    })).sort((a, b) => b.score - a.score);

    return {
      status: "tidak_ditemukan",
      pesan: "Maaf, saya belum memiliki informasi untuk pertanyaan tersebut.",
      rekomendasi: allSorted.slice(0, 3).map((c) => c.item.pertanyaan),
    };
  }

  return {
    status: "berhasil",
    pertanyaan: best.item.pertanyaan,
    jawaban: best.item.jawaban,
    kategori: best.item.kategori,
    similarity: best.score.toFixed(3),
  };
}
