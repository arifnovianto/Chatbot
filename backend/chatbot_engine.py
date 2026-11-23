"""
chatbot_engine.py
TF-IDF engine untuk FAQ PPAT ATR/BPN.

Single source of truth: data/konten.json
  - Dibaca backend untuk TF-IDF
  - Disajikan ke frontend via GET /konten
  - Tambah/edit konten = edit konten.json saja
"""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords", quiet=True)
_STOP_WORDS = set(stopwords.words("indonesian"))

# Path ke file JSON
_KONTEN_PATH = Path(__file__).parent / "data" / "konten.json"


def _load_konten() -> list[dict]:
    """Baca konten.json dan kembalikan sebagai list."""
    with open(_KONTEN_PATH, encoding="utf-8") as f:
        return json.load(f)


def _build_dataset(konten: list[dict]) -> pd.DataFrame:
    """
    Ekstrak setiap seksi dari konten.json menjadi baris dataset.
    judul seksi  → 'pertanyaan'
    isi seksi    → 'jawaban'
    label topik  → 'kategori'
    """
    rows = []
    for topik in konten:
        kategori = topik["label"]
        for seksi in topik.get("seksi", []):
            rows.append({
                "pertanyaan": seksi["judul"],
                "jawaban":    seksi["isi"],
                "kategori":   kategori,
                "sumber":     f"Portal ATR/BPN — {kategori}",
            })
    return pd.DataFrame(rows)


# ════════════════════════════════════════════════════════════
# ENGINE
# ════════════════════════════════════════════════════════════

class ChatbotEngine:
    def __init__(self):
        self._konten = _load_konten()
        self.df = _build_dataset(self._konten)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.model = LogisticRegression(max_iter=1000, class_weight="balanced")
        self._train()
        print(f"[Engine] {len(self.df)} dokumen | "
              f"{self.df['kategori'].nunique()} kategori | "
              f"sumber: konten.json")

    # ── Preprocessing ────────────────────────────────────────
    def _preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        words = [w for w in text.split() if w not in _STOP_WORDS]
        return " ".join(words)

    # ── Training TF-IDF + LogReg ─────────────────────────────
    def _train(self):
        self.df["teks_bersih"] = self.df["pertanyaan"].apply(self._preprocess)
        self.X_tfidf = self.vectorizer.fit_transform(self.df["teks_bersih"])
        self.model.fit(self.X_tfidf, self.df["kategori"])

    # ── Reload konten.json (tanpa restart server) ─────────────
    def reload(self) -> int:
        self._konten = _load_konten()
        self.df = _build_dataset(self._konten)
        self._train()
        print(f"[Engine] Reload: {len(self.df)} dokumen")
        return len(self.df)

    # ── Tambah data baru & retrain ───────────────────────────
    def tambah_pengetahuan(self, pertanyaan: str, jawaban: str,
                           kategori: str, sumber: str) -> int:
        new_row = pd.DataFrame({
            "pertanyaan":  [pertanyaan],
            "jawaban":     [jawaban],
            "kategori":    [kategori],
            "sumber":      [sumber],
            "teks_bersih": [self._preprocess(pertanyaan)],
        })
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self._train()
        return len(self.df)

    # ── Getter konten mentah (untuk frontend) ────────────────
    def get_konten(self) -> list[dict]:
        return self._konten

    def get_categories(self) -> list[str]:
        return sorted(self.df["kategori"].unique().tolist())

    # ── Cari jawaban ─────────────────────────────────────────
    def cari_jawaban(self, pertanyaan: str,
                     kategori_filter: str | None = None) -> dict:
        bersih = self._preprocess(pertanyaan)
        if not bersih.strip():
            return {"status": "kosong", "pesan": "Pertanyaan tidak boleh kosong."}

        query_vec = self.vectorizer.transform([bersih])

        # Tentukan pool kandidat
        if kategori_filter and kategori_filter in self.df["kategori"].values:
            pool = self.df[self.df["kategori"] == kategori_filter].copy()
        else:
            predicted_cat = self.model.predict(query_vec)[0]
            pool = self.df[self.df["kategori"] == predicted_cat].copy()

        pool_vecs  = self.vectorizer.transform(pool["teks_bersih"])
        scores     = cosine_similarity(query_vec, pool_vecs)[0]
        best_idx   = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        # Similarity terlalu rendah → tampilkan rekomendasi
        if best_score < 0.15:
            all_vecs   = self.vectorizer.transform(self.df["teks_bersih"])
            all_scores = cosine_similarity(query_vec, all_vecs)[0]
            top_idx    = np.argsort(all_scores)[::-1][:3]
            rekomendasi = [
                self.df.iloc[i]["pertanyaan"]
                for i in top_idx if all_scores[i] > 0.0
            ]
            if not rekomendasi:
                rekomendasi = self.df["pertanyaan"].sample(3).tolist()

            return {
                "status": "tidak_ditemukan",
                "pesan": "Maaf, saya belum memiliki informasi untuk pertanyaan tersebut. "
                         "Silakan hubungi Helpdesk ATR/BPN di helpdesk@atrbpn.go.id.",
                "kategori": pool["kategori"].iloc[0] if len(pool) else "Umum",
                "similarity": round(best_score, 3),
                "rekomendasi": rekomendasi,
            }

        row = pool.iloc[best_idx]
        return {
            "status":           "berhasil",
            "pertanyaan_cocok": row["pertanyaan"],
            "jawaban":          row["jawaban"],
            "kategori":         row["kategori"],
            "sumber":           row["sumber"],
            "similarity":       round(best_score, 3),
        }


# Singleton
engine = ChatbotEngine()
