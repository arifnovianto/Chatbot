"""
chatbot_engine.py
Mesin TF-IDF + Cosine Similarity untuk FAQ PPAT ATR/BPN.
Dijalankan sekali saat startup FastAPI (singleton).
"""

import re
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

# ── Download stopwords sekali ────────────────────────────────
nltk.download("stopwords", quiet=True)
_STOP_WORDS = set(stopwords.words("indonesian"))

# ════════════════════════════════════════════════════════════
# DATASET
# ════════════════════════════════════════════════════════════

_DATA = {
    "pertanyaan": [
        # Akun, Kredensial & Autentikasi
        "Mengapa akun Mitra PPAT tidak bisa login ke Portal SSO?",
        "Apa penyebab akun PPAT terblokir di Portal SSO?",
        "Bagaimana cara reset password akun Portal SSO PPAT?",
        "Bagaimana cara mendaftarkan akun PPAT baru di portal mitra?",
        "Kenapa kode OTP tidak masuk ke nomor HP saat login?",
        "Bagaimana cara mengubah nomor HP yang terdaftar di akun PPAT?",
        # Pembuatan Akta & Validasi
        "Mengapa muncul pesan error saat membuat akta jual beli di portal?",
        "Bagaimana cara mengatasi pesan error validasi data pihak di portal?",
        "Mengapa nomor sertifikat tidak ditemukan saat validasi di sistem?",
        "Bagaimana format penulisan nomor hak yang benar di portal ATR/BPN?",
        "Bagaimana cara mencetak draft akta dari portal mitra PPAT?",
        "Apa yang harus dilakukan jika data bidang tanah tidak muncul di portal?",
        # Peralihan Hak Elektronik & Pembayaran
        "Bagaimana cara mengajukan permohonan peralihan hak secara elektronik?",
        "Apa saja dokumen yang dibutuhkan untuk peralihan hak elektronik?",
        "Berapa lama proses peralihan hak elektronik di BPN?",
        "Mengapa kode billing SPS peralihan hak tidak muncul di portal?",
        "Mengapa surat pengantar berkas peralihan hak tidak bisa dicetak?",
        "Bagaimana cara mengecek status permohonan peralihan hak elektronik?",
        # Pelaporan Kendala Teknis
        "Ke mana PPAT harus melaporkan kendala teknis portal mitra?",
        "Bagaimana cara mengajukan tiket pengaduan melalui ANDALAS?",
        "Bagaimana cara menghubungi helpdesk ATR/BPN untuk kendala portal?",
        "Apakah tersedia panduan pengguna portal mitra PPAT?",
        # Hak Tanggungan Elektronik
        "Apa itu Hak Tanggungan Elektronik di portal ATR/BPN?",
        "Bagaimana cara mendaftarkan Hak Tanggungan secara elektronik?",
        "Berapa biaya pendaftaran Hak Tanggungan Elektronik?",
        "Mengapa APHT tidak bisa diajukan secara elektronik?",
        # KJKSB
        "Apa itu KJKSB dalam layanan pertanahan ATR/BPN?",
        "Bagaimana cara mengakses layanan KJKSB melalui portal?",
        "Dokumen apa saja yang diperlukan untuk permohonan KJKSB?",
        # KKPR Non Berusaha & Stranas
        "Apa itu KKPR Non Berusaha dalam layanan ATR/BPN?",
        "Bagaimana cara mengajukan permohonan KKPR Non Berusaha?",
        "Apa itu Stranas dalam konteks layanan pertanahan?",
        "Bagaimana cara PPAT mendukung program Stranas di portal?",
    ],
    "jawaban": [
        # Akun, Kredensial & Autentikasi
        "Akun Mitra PPAT tidak bisa login ke Portal SSO umumnya disebabkan oleh: (1) Masa berlaku SK Pengangkatan/Perpanjangan sudah habis; (2) Data PPAT belum diperbarui di sistem Ditjen Penetapan Hak dan Pendaftaran Tanah; (3) Password salah atau akun terkunci. Pastikan SK masih aktif dan data sudah diperbarui oleh Kantor Pertanahan setempat.",
        "Akun PPAT dapat terblokir jika terjadi percobaan login yang gagal berulang kali (lebih dari 5 kali), atau jika sistem mendeteksi aktivitas mencurigakan. Tunggu 30 menit lalu coba lagi, atau ajukan pembukaan blokir melalui Helpdesk ATR/BPN.",
        "Reset password dapat dilakukan di halaman login Portal SSO dengan mengklik tombol 'Lupa Password'. Masukkan alamat email terdaftar, lalu ikuti tautan yang dikirimkan ke email tersebut. Tautan berlaku selama 24 jam.",
        "Pendaftaran akun PPAT baru dilakukan melalui Kantor Pertanahan setempat. PPAT membawa SK Pengangkatan asli beserta dokumen pendukung. Petugas akan mendaftarkan akun ke sistem SSO dan mengirimkan kredensial awal ke email resmi PPAT.",
        "Kode OTP tidak masuk dapat disebabkan: nomor HP tidak terdaftar di sistem, gangguan jaringan provider, atau delay pengiriman SMS. Klik 'Kirim Ulang OTP' setelah 60 detik. Jika masalah berlanjut, hubungi Helpdesk untuk memverifikasi nomor HP terdaftar.",
        "Perubahan nomor HP terdaftar di akun PPAT harus dilakukan melalui Kantor Pertanahan setempat dengan membawa identitas diri dan SK PPAT. Petugas akan memperbarui data di sistem SSO.",
        # Pembuatan Akta & Validasi
        "Pesan error saat membuat akta jual beli umumnya terjadi karena: (1) Data bidang tanah belum lengkap atau NIK pihak tidak valid di database Dukcapil; (2) Sesi login sudah habis (timeout); (3) Format input tidak sesuai. Lakukan logout lalu login kembali, periksa kelengkapan data, dan pastikan NIK sesuai KTP aktif.",
        "Error validasi data pihak biasanya disebabkan NIK tidak terdaftar di Dukcapil atau terdapat ketidaksesuaian nama. Pastikan NIK diinput dengan benar dan sesuai KTP. Jika NIK valid namun tetap error, laporkan ke Helpdesk disertai tangkapan layar pesan error.",
        "Nomor sertifikat tidak ditemukan di sistem dapat berarti: (1) Data belum ter-digitasi; (2) Sertifikat diterbitkan oleh kantor pertanahan lain; (3) Terdapat kesalahan penulisan nomor. Konfirmasi kebenaran nomor dan wilayah ke Kantor Pertanahan penerbit sertifikat.",
        "Format nomor hak yang benar mengikuti pola: [Kode Kabupaten/Kota].[Kode Kecamatan].[Jenis Hak].[Nomor Urut], contoh: 3273.010.SHM.00123. Pastikan tidak ada spasi, titik tambahan, atau karakter khusus.",
        "Untuk mencetak draft akta, buka menu 'Daftar Akta', pilih akta yang dimaksud, lalu klik tombol 'Unduh Draft PDF'. Pastikan browser mengizinkan pop-up dari domain portal. Gunakan Chrome atau Firefox versi terbaru.",
        "Jika data bidang tanah tidak muncul, kemungkinan data bidang belum terpetakan ke wilayah kerja PPAT, atau terdapat kesalahan kode wilayah. Hubungi petugas Kantor Pertanahan untuk memastikan bidang tanah telah terdaftar dan terpetakan dengan benar.",
        # Peralihan Hak Elektronik & Pembayaran
        "Pengajuan peralihan hak elektronik dilakukan melalui: (1) Login ke portal mitra PPAT; (2) Pilih menu 'Layanan Elektronik' → 'Peralihan Hak'; (3) Isi formulir permohonan dan unggah dokumen persyaratan; (4) Bayar kode billing yang dihasilkan sistem; (5) Pantau status melalui menu Tracking Permohonan.",
        "Dokumen persyaratan peralihan hak elektronik meliputi: sertifikat asli, akta PPAT terkait, KTP seluruh pihak, bukti pembayaran BPHTB dan PPh Final, surat pernyataan sesuai jenis peralihan, serta dokumen pendukung lain sesuai ketentuan Kantor Pertanahan setempat.",
        "Proses peralihan hak elektronik umumnya diselesaikan dalam 5–7 hari kerja setelah berkas dinyatakan lengkap dan valid oleh petugas Kantor Pertanahan. Waktu dapat berbeda tergantung antrean dan kebijakan masing-masing Kantor Pertanahan.",
        "Kode billing SPS tidak muncul biasanya karena: (1) Data formulir permohonan belum lengkap atau masih berstatus draft; (2) Sistem SPS sedang dalam pemeliharaan. Pastikan semua field wajib terisi, simpan permohonan, lalu muat ulang halaman.",
        "Surat pengantar berkas yang tidak bisa dicetak dapat disebabkan status permohonan belum diverifikasi oleh petugas, atau koneksi internet tidak stabil. Periksa status permohonan di menu Tracking, lalu coba cetak ulang setelah status berubah menjadi 'Siap Cetak'.",
        "Status permohonan peralihan hak dapat dipantau melalui menu 'Tracking Permohonan' di portal dengan memasukkan nomor berkas yang diperoleh saat pendaftaran. Notifikasi perubahan status juga dikirimkan melalui email terdaftar.",
        # Pelaporan Kendala Teknis
        "Kendala teknis portal PPAT dapat dilaporkan melalui: (1) Fitur Tiket Pengaduan ANDALAS di portal; (2) Email helpdesk@atrbpn.go.id; (3) Call Center Kementerian ATR/BPN; (4) Media sosial resmi @kementerian_atrbpn. Sertakan tangkapan layar saat melapor.",
        "Tiket pengaduan ANDALAS diajukan melalui menu 'Tiket Pengaduan' di portal. Pilih kategori masalah, deskripsikan kendala secara detail, lampirkan tangkapan layar jika ada, lalu klik Kirim. Nomor tiket dikirimkan ke email untuk pemantauan.",
        "Helpdesk ATR/BPN dapat dihubungi melalui portal Sentuh Tanahku, email helpdesk@atrbpn.go.id, atau melalui bantuan.atrbpn.go.id. Jam layanan Helpdesk adalah Senin–Jumat pukul 08.00–16.00 WIB.",
        "Panduan pengguna portal Mitra PPAT tersedia di menu 'Bantuan' → 'Unduh Panduan' di portal, atau melalui bantuan.atrbpn.go.id pada bagian Tanya Jawab (FAQ) dan artikel panduan teknis.",
        # Hak Tanggungan Elektronik
        "Hak Tanggungan Elektronik (HT-el) adalah layanan pendaftaran hak tanggungan secara daring yang diintegrasikan dalam Portal Mitra ATR/BPN, memungkinkan PPAT mendaftarkan APHT dan SKMHT tanpa harus datang ke kantor pertanahan.",
        "Pendaftaran Hak Tanggungan Elektronik dilakukan melalui: (1) Login portal mitra PPAT; (2) Pilih menu 'Hak Tanggungan Elektronik'; (3) Isi data debitur, kreditur, dan objek jaminan; (4) Unggah APHT dan dokumen pendukung; (5) Bayar PNBP melalui kode billing; (6) Pantau status pendaftaran.",
        "Biaya PNBP pendaftaran Hak Tanggungan Elektronik dihitung berdasarkan nilai tanggungan sesuai Peraturan Pemerintah tentang PNBP Kementerian ATR/BPN. Rincian tarif dapat dilihat di kalkulator PNBP yang tersedia di portal.",
        "APHT tidak bisa diajukan secara elektronik biasanya karena: (1) Data sertifikat belum ter-mapping di sistem HT-el; (2) PPAT belum terdaftar sebagai pengguna layanan HT-el; (3) Terdapat ketidaksesuaian data kreditur dengan sistem OJK.",
        # KJKSB
        "KJKSB (Kegiatan Jual-beli, Kredit, Sewa-menyewa, dan Berbagi) adalah layanan pencatatan transaksi pertanahan berbasis digital di portal ATR/BPN untuk meningkatkan transparansi dan pengawasan transaksi properti di Indonesia.",
        "Layanan KJKSB dapat diakses melalui menu 'KJKSB' di portal mitra PPAT setelah login menggunakan akun SSO. Pilih jenis transaksi yang sesuai, isi data pihak dan objek tanah, lalu ikuti alur pengisian yang tersedia.",
        "Dokumen yang diperlukan untuk permohonan KJKSB meliputi: identitas para pihak (KTP/Paspor), dokumen kepemilikan tanah (sertifikat), akta/perjanjian terkait transaksi, bukti pembayaran pajak, serta dokumen pendukung sesuai jenis kegiatan.",
        # KKPR Non Berusaha & Stranas
        "KKPR Non Berusaha (Kesesuaian Kegiatan Pemanfaatan Ruang untuk Non Usaha) adalah persetujuan pemanfaatan ruang untuk kegiatan non-komersial, seperti pembangunan rumah tinggal atau fasilitas sosial oleh perorangan.",
        "Permohonan KKPR Non Berusaha diajukan secara daring melalui portal OSS di oss.go.id atau melalui dinas terkait. PPAT dapat membantu klien mempersiapkan dokumen teknis seperti peta bidang dan data kepemilikan tanah.",
        "Stranas (Strategi Nasional) dalam konteks pertanahan merujuk pada program prioritas nasional yang meliputi redistribusi tanah, legalisasi aset, dan penyelesaian konflik agraria sebagai bagian dari Reforma Agraria yang dikoordinasikan Kementerian ATR/BPN.",
        "PPAT dapat mendukung program Stranas melalui portal dengan melaporkan transaksi pertanahan terkait objek redistribusi atau legalisasi aset menggunakan menu 'Laporan Stranas' yang tersedia bagi PPAT di lokus program Stranas.",
    ],
    "kategori": [
        *["Akun, Kredensial & Autentikasi"] * 6,
        *["Pembuatan Akta & Validasi"] * 6,
        *["Peralihan Hak Elektronik & Pembayaran"] * 6,
        *["Pelaporan Kendala Teknis"] * 4,
        *["Hak Tanggungan Elektronik"] * 4,
        *["KJKSB"] * 3,
        *["KKPR Non Berusaha & Stranas"] * 4,
    ],
    "sumber": [
        *["FAQ PPAT ATR/BPN — Akun, Kredensial & Autentikasi"] * 6,
        *["FAQ PPAT ATR/BPN — Pembuatan Akta & Validasi"] * 6,
        *["FAQ PPAT ATR/BPN — Peralihan Hak Elektronik & Pembayaran"] * 6,
        *["FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis"] * 4,
        *["FAQ PPAT ATR/BPN — Hak Tanggungan Elektronik"] * 4,
        *["FAQ PPAT ATR/BPN — KJKSB"] * 3,
        *["FAQ PPAT ATR/BPN — KKPR Non Berusaha & Stranas"] * 4,
    ],
}

# ════════════════════════════════════════════════════════════
# ENGINE CLASS
# ════════════════════════════════════════════════════════════

class ChatbotEngine:
    """
    Singleton engine — training terjadi sekali saat import.
    Bisa dipanggil ulang retrain() jika data ditambah.
    """

    def __init__(self):
        self.df = pd.DataFrame(_DATA)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.model = LogisticRegression(max_iter=1000, class_weight="balanced")
        self._train()

    # ── Preprocessing ────────────────────────────────────────
    def _preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        words = [w for w in text.split() if w not in _STOP_WORDS]
        return " ".join(words)

    # ── Training ─────────────────────────────────────────────
    def _train(self):
        self.df["pertanyaan_bersih"] = self.df["pertanyaan"].apply(self._preprocess)
        X = self.df["pertanyaan_bersih"]
        y = self.df["kategori"]
        self.X_tfidf = self.vectorizer.fit_transform(X)
        self.model.fit(self.X_tfidf, y)

    # ── Tambah data baru & retrain ───────────────────────────
    def tambah_pengetahuan(
        self,
        pertanyaan: str,
        jawaban: str,
        kategori: str,
        sumber: str,
    ) -> int:
        new_row = pd.DataFrame(
            {
                "pertanyaan": [pertanyaan],
                "jawaban": [jawaban],
                "kategori": [kategori],
                "sumber": [sumber],
                "pertanyaan_bersih": [self._preprocess(pertanyaan)],
            }
        )
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self._train()
        return len(self.df)

    # ── Daftar kategori ──────────────────────────────────────
    def get_categories(self) -> list[str]:
        return sorted(self.df["kategori"].unique().tolist())

    # ── Cari jawaban ─────────────────────────────────────────
    def cari_jawaban(self, pertanyaan: str, kategori_filter: str | None = None) -> dict:
        bersih = self._preprocess(pertanyaan)
        if not bersih.strip():
            return {"status": "kosong", "pesan": "Pertanyaan tidak boleh kosong."}

        query_vec = self.vectorizer.transform([bersih])

        # Tentukan pool kandidat
        if kategori_filter and kategori_filter in self.df["kategori"].values:
            pool = self.df[self.df["kategori"] == kategori_filter].copy()
        else:
            # Gunakan prediksi kategori dari LogisticRegression
            predicted_cat = self.model.predict(query_vec)[0]
            pool = self.df[self.df["kategori"] == predicted_cat].copy()

        # Hitung cosine similarity dalam pool
        pool_vecs = self.vectorizer.transform(pool["pertanyaan_bersih"])
        scores = cosine_similarity(query_vec, pool_vecs)[0]
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        # Threshold rendah → kembalikan rekomendasi
        if best_score < 0.20:
            all_vecs = self.vectorizer.transform(self.df["pertanyaan_bersih"])
            all_scores = cosine_similarity(query_vec, all_vecs)[0]
            top_idx = np.argsort(all_scores)[::-1][:3]
            rekomendasi = [
                self.df.iloc[i]["pertanyaan"]
                for i in top_idx
                if all_scores[i] > 0.0
            ]
            if not rekomendasi:
                rekomendasi = self.df["pertanyaan"].sample(3).tolist()

            return {
                "status": "tidak_ditemukan",
                "pesan": "Maaf, saya belum memiliki informasi untuk pertanyaan tersebut. Silakan hubungi Helpdesk ATR/BPN.",
                "kategori": pool["kategori"].iloc[0] if len(pool) else "Umum",
                "similarity": round(best_score, 3),
                "rekomendasi": rekomendasi,
            }

        row = pool.iloc[best_idx]
        return {
            "status": "berhasil",
            "pertanyaan_cocok": row["pertanyaan"],
            "jawaban": row["jawaban"],
            "kategori": row["kategori"],
            "sumber": row["sumber"],
            "similarity": round(best_score, 3),
        }


# ── Singleton — dipakai langsung oleh main.py ────────────────
engine = ChatbotEngine()
