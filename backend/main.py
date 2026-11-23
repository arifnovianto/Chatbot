"""
main.py — FastAPI entry point
Jalankan: uvicorn main:app --reload --port 8000
Docs    : http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chatbot_engine import engine

# ════════════════════════════════════════════════════════════
# APP
# ════════════════════════════════════════════════════════════

app = FastAPI(
    title="BPN-Bot API",
    description="FAQ Chatbot Portal PPAT ATR/BPN — TF-IDF + Cosine Similarity",
    version="1.0.0",
)

# ── CORS (izinkan React dev server) ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev mode: izinkan semua origin
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ════════════════════════════════════════════════════════════
# SCHEMAS
# ════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    pertanyaan: str = Field(..., min_length=2, max_length=500, example="Kenapa akun PPAT saya tidak bisa login?")
    kategori: str | None = Field(None, example="Akun, Kredensial & Autentikasi")

class TambahRequest(BaseModel):
    pertanyaan: str = Field(..., min_length=5)
    jawaban: str = Field(..., min_length=10)
    kategori: str = Field(..., min_length=2)
    sumber: str = Field(..., min_length=2)

# ════════════════════════════════════════════════════════════
# ENDPOINTS
# ════════════════════════════════════════════════════════════

@app.get("/", tags=["Health"])
def root():
    """Health check."""
    return {"status": "ok", "app": "BPN-Bot API", "version": "1.0.0"}


@app.get("/categories", tags=["Info"])
def get_categories():
    return {"kategori": engine.get_categories()}


@app.get("/konten", tags=["Info"])
def get_konten():
    """
    Kembalikan seluruh konten artikel dari konten.json.
    Dipakai frontend untuk render sidebar dan halaman utama.
    """
    return engine.get_konten()


@app.post("/reload", tags=["Admin"])
def reload_konten():
    """
    Reload konten.json tanpa restart server.
    Panggil endpoint ini setelah edit konten.json.
    """
    total = engine.reload()
    return {
        "status": "berhasil",
        "pesan": f"Konten berhasil di-reload. Total dokumen: {total}.",
        "total": total,
    }


@app.post("/chat", tags=["Chat"])
def chat(req: ChatRequest):
    """
    Terima pertanyaan → kembalikan jawaban terbaik dari database FAQ.

    - `pertanyaan` : teks pertanyaan pengguna
    - `kategori`   : (opsional) filter kategori spesifik
    """
    if not req.pertanyaan.strip():
        raise HTTPException(status_code=400, detail="Pertanyaan tidak boleh kosong.")

    hasil = engine.cari_jawaban(
        pertanyaan=req.pertanyaan.strip(),
        kategori_filter=req.kategori,
    )
    return hasil


@app.post("/tambah", tags=["Admin"])
def tambah_pengetahuan(req: TambahRequest):
    """
    Tambah data FAQ baru ke database dan retrain model TF-IDF.
    Gunakan endpoint ini untuk memperluas knowledge base.
    """
    total = engine.tambah_pengetahuan(
        pertanyaan=req.pertanyaan.strip(),
        jawaban=req.jawaban.strip(),
        kategori=req.kategori.strip(),
        sumber=req.sumber.strip(),
    )
    return {
        "status": "berhasil",
        "pesan": f"Data berhasil ditambahkan. Total database: {total} pertanyaan.",
        "total": total,
    }


@app.get("/stats", tags=["Info"])
def stats():
    """Statistik database FAQ yang sedang aktif."""
    df = engine.df
    per_kategori = df["kategori"].value_counts().to_dict()
    return {
        "total_pertanyaan": len(df),
        "total_kategori": df["kategori"].nunique(),
        "per_kategori": per_kategori,
    }
