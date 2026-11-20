// chatEngine.js — Panggil FastAPI backend
const BASE_URL = "http://localhost:8000";

export async function cariJawaban(pertanyaan, kategoriFilter = null) {
  const body = {
    pertanyaan: pertanyaan.trim(),
    ...(kategoriFilter && kategoriFilter !== "semua"
      ? { kategori: kategoriFilter }
      : {}),
  };

  let res;
  try {
    res = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (err) {
    console.error("[chatEngine] fetch gagal:", err);
    return {
      status: "error",
      pesan: `Tidak dapat terhubung ke server (${err.message}). Pastikan backend berjalan di port 8000.`,
    };
  }

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    console.error("[chatEngine] server error:", res.status, errBody);
    return {
      status: "error",
      pesan: errBody.detail || `Server error: ${res.status}`,
    };
  }

  return await res.json();
}

export async function fetchCategories() {
  try {
    const res = await fetch(`${BASE_URL}/categories`);
    if (!res.ok) return [];
    const data = await res.json();
    return data.kategori ?? [];
  } catch (err) {
    console.error("[chatEngine] fetchCategories gagal:", err);
    return [];
  }
}
