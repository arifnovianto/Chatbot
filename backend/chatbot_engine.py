"""
chatbot_engine.py
Mesin TF-IDF + Cosine Similarity untuk FAQ PPAT ATR/BPN.

Dataset mencakup DUA sumber:
  1. Q&A eksplisit  — pertanyaan + jawaban langsung
  2. Konten artikel — teks penjelasan dari sidebar (diekstrak
     menjadi pasangan pertanyaan-implisit + jawaban agar bisa
     di-index oleh TF-IDF)
"""

import re
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords", quiet=True)
_STOP_WORDS = set(stopwords.words("indonesian"))

# ════════════════════════════════════════════════════════════
# DATASET — Q&A Eksplisit
# ════════════════════════════════════════════════════════════

_QA = [
    # ── Akun, Kredensial & Autentikasi ──────────────────────
    ("Mengapa akun Mitra PPAT tidak bisa login ke Portal SSO?",
     "Akun Mitra PPAT tidak bisa login ke Portal SSO umumnya disebabkan oleh: (1) Masa berlaku SK Pengangkatan/Perpanjangan sudah habis; (2) Data PPAT belum diperbarui di sistem Ditjen Penetapan Hak; (3) Password salah atau akun terkunci. Pastikan SK masih aktif dan data sudah diperbarui oleh Kantor Pertanahan setempat.",
     "Akun, Kredensial & Autentikasi"),

    ("Apa penyebab akun PPAT terblokir di Portal SSO?",
     "Akun PPAT terblokir jika percobaan login gagal lebih dari 5 kali berturut-turut, atau sistem mendeteksi aktivitas mencurigakan. Tunggu 30 menit lalu coba lagi, atau ajukan pembukaan blokir melalui Helpdesk ATR/BPN.",
     "Akun, Kredensial & Autentikasi"),

    ("Bagaimana cara reset password akun Portal SSO PPAT?",
     "Reset password dilakukan di halaman login Portal SSO: klik 'Lupa Password', masukkan email terdaftar, lalu ikuti tautan yang dikirim ke email. Tautan berlaku 24 jam.",
     "Akun, Kredensial & Autentikasi"),

    ("Bagaimana cara mendaftarkan akun PPAT baru di portal mitra?",
     "Pendaftaran akun PPAT baru dilakukan melalui Kantor Pertanahan setempat dengan membawa SK Pengangkatan asli. Petugas mendaftarkan akun ke sistem SSO dan mengirimkan kredensial awal ke email resmi PPAT.",
     "Akun, Kredensial & Autentikasi"),

    ("Kenapa kode OTP tidak masuk ke nomor HP saat login?",
     "Kode OTP tidak masuk bisa disebabkan nomor HP tidak terdaftar, gangguan jaringan provider, atau delay SMS. Klik 'Kirim Ulang OTP' setelah 60 detik. Jika masalah berlanjut, hubungi Helpdesk.",
     "Akun, Kredensial & Autentikasi"),

    ("Bagaimana cara mengubah nomor HP yang terdaftar di akun PPAT?",
     "Perubahan nomor HP dilakukan melalui Kantor Pertanahan setempat dengan membawa identitas diri dan SK PPAT. Petugas akan memperbarui data di sistem SSO.",
     "Akun, Kredensial & Autentikasi"),

    # ── Pembuatan Akta & Validasi ────────────────────────────
    ("Mengapa muncul pesan error saat membuat akta jual beli di portal?",
     "Error saat membuat akta terjadi karena: (1) Data bidang tanah belum lengkap atau NIK tidak valid di Dukcapil; (2) Sesi login sudah habis; (3) Format input tidak sesuai. Logout lalu login kembali dan periksa kelengkapan data.",
     "Pembuatan Akta & Validasi"),

    ("Mengapa nomor sertifikat tidak ditemukan saat validasi di sistem?",
     "Nomor sertifikat tidak ditemukan bisa berarti data belum ter-digitasi, sertifikat dari kantor pertanahan lain, atau kesalahan penulisan nomor. Konfirmasi ke Kantor Pertanahan penerbit sertifikat.",
     "Pembuatan Akta & Validasi"),

    ("Bagaimana format penulisan nomor hak yang benar di portal ATR/BPN?",
     "Format nomor hak: [Kode Kab/Kota].[Kode Kecamatan].[Jenis Hak].[Nomor Urut], contoh: 3273.010.SHM.00123. Tidak boleh ada spasi atau karakter khusus.",
     "Pembuatan Akta & Validasi"),

    ("Bagaimana cara mencetak draft akta dari portal mitra PPAT?",
     "Buka menu 'Daftar Akta', pilih akta, lalu klik 'Unduh Draft PDF'. Pastikan browser mengizinkan pop-up dari portal. Gunakan Chrome atau Firefox terbaru.",
     "Pembuatan Akta & Validasi"),

    ("Apa yang harus dilakukan jika data bidang tanah tidak muncul di portal?",
     "Data bidang tanah tidak muncul kemungkinan karena belum terpetakan ke wilayah kerja PPAT atau kesalahan kode wilayah. Hubungi Kantor Pertanahan untuk memastikan data terdaftar dengan benar.",
     "Pembuatan Akta & Validasi"),

    ("Bagaimana cara mengatasi error validasi NIK di portal?",
     "Error validasi NIK biasanya karena NIK tidak terdaftar di Dukcapil atau nama tidak sesuai. Pastikan NIK dari KTP aktif. Jika tetap error, laporkan ke Helpdesk disertai tangkapan layar.",
     "Pembuatan Akta & Validasi"),

    # ── Peralihan Hak Elektronik & Pembayaran ───────────────
    ("Bagaimana cara mengajukan permohonan peralihan hak secara elektronik?",
     "Pengajuan peralihan hak elektronik: (1) Login portal; (2) Menu Layanan Elektronik → Peralihan Hak; (3) Isi formulir dan unggah dokumen; (4) Bayar kode billing SPS; (5) Pantau di menu Tracking Permohonan.",
     "Peralihan Hak Elektronik & Pembayaran"),

    ("Apa saja dokumen yang dibutuhkan untuk peralihan hak elektronik?",
     "Dokumen peralihan hak elektronik: sertifikat asli, akta PPAT, KTP para pihak, bukti BPHTB dan PPh Final, surat pernyataan sesuai jenis peralihan, dan dokumen tambahan sesuai ketentuan Kantor Pertanahan.",
     "Peralihan Hak Elektronik & Pembayaran"),

    ("Berapa lama proses peralihan hak elektronik di BPN?",
     "Proses peralihan hak elektronik umumnya 5–7 hari kerja setelah berkas dinyatakan lengkap. Waktu bervariasi tergantung antrean masing-masing Kantor Pertanahan.",
     "Peralihan Hak Elektronik & Pembayaran"),

    ("Mengapa kode billing SPS peralihan hak tidak muncul di portal?",
     "Kode billing SPS tidak muncul karena formulir belum lengkap atau sistem SPS sedang maintenance. Isi semua field wajib, simpan, lalu muat ulang halaman.",
     "Peralihan Hak Elektronik & Pembayaran"),

    ("Mengapa surat pengantar berkas peralihan hak tidak bisa dicetak?",
     "Surat pengantar tidak bisa dicetak karena permohonan belum diverifikasi petugas atau koneksi tidak stabil. Cek status di Tracking — cetak setelah status berubah menjadi 'Siap Cetak'.",
     "Peralihan Hak Elektronik & Pembayaran"),

    ("Bagaimana cara mengecek status permohonan peralihan hak elektronik?",
     "Pantau status melalui menu Tracking Permohonan dengan memasukkan nomor berkas. Notifikasi perubahan status juga dikirim ke email terdaftar.",
     "Peralihan Hak Elektronik & Pembayaran"),

    # ── Pelaporan Kendala Teknis ─────────────────────────────
    ("Ke mana PPAT harus melaporkan kendala teknis portal mitra?",
     "Kendala teknis dilaporkan melalui: (1) Tiket Pengaduan ANDALAS di portal; (2) Email helpdesk@atrbpn.go.id; (3) Call Center ATR/BPN. Sertakan tangkapan layar saat melapor.",
     "Pelaporan Kendala Teknis"),

    ("Bagaimana cara mengajukan tiket pengaduan melalui ANDALAS?",
     "Tiket ANDALAS: menu Tiket Pengaduan → Buat Tiket Baru → pilih kategori → deskripsikan masalah → lampirkan tangkapan layar → Kirim. Nomor tiket dikirim ke email.",
     "Pelaporan Kendala Teknis"),

    ("Bagaimana cara menghubungi helpdesk ATR/BPN?",
     "Helpdesk ATR/BPN: email helpdesk@atrbpn.go.id, portal Sentuh Tanahku, atau bantuan.atrbpn.go.id. Jam layanan Senin–Jumat 08.00–16.00 WIB.",
     "Pelaporan Kendala Teknis"),

    ("Apakah tersedia panduan pengguna portal mitra PPAT?",
     "Panduan tersedia di menu Bantuan → Unduh Panduan di portal, atau di bantuan.atrbpn.go.id bagian FAQ dan artikel panduan teknis.",
     "Pelaporan Kendala Teknis"),

    # ── Hak Tanggungan Elektronik ────────────────────────────
    ("Apa itu Hak Tanggungan Elektronik?",
     "HT-el adalah layanan pendaftaran hak tanggungan secara daring di Portal Mitra ATR/BPN. PPAT dapat mendaftarkan APHT dan SKMHT tanpa datang ke kantor pertanahan. Dasar hukum: Permen ATR/BPN No. 5 Tahun 2020.",
     "Hak Tanggungan Elektronik"),

    ("Bagaimana cara mendaftarkan Hak Tanggungan secara elektronik?",
     "Langkah HT-el: (1) Login portal; (2) Menu Hak Tanggungan Elektronik; (3) Isi data debitur, kreditur, objek jaminan; (4) Unggah APHT; (5) Bayar PNBP via kode billing; (6) Pantau status.",
     "Hak Tanggungan Elektronik"),

    ("Berapa biaya PNBP pendaftaran Hak Tanggungan Elektronik?",
     "Biaya PNBP HT-el dihitung otomatis berdasarkan nilai tanggungan sesuai PP tentang PNBP ATR/BPN. Gunakan kalkulator PNBP di halaman formulir HT-el untuk simulasi biaya.",
     "Hak Tanggungan Elektronik"),

    ("Mengapa APHT tidak bisa diajukan secara elektronik?",
     "APHT tidak bisa diajukan elektronik karena: data sertifikat belum ter-mapping di sistem HT-el, PPAT belum terdaftar sebagai pengguna HT-el, atau ketidaksesuaian data kreditur dengan sistem OJK. Hubungi Kantor Pertanahan untuk aktivasi.",
     "Hak Tanggungan Elektronik"),

    ("Bagaimana cara aktivasi akses layanan HT-el?",
     "Aktivasi layanan HT-el dilakukan melalui Kantor Pertanahan setempat. Pastikan data sertifikat objek jaminan sudah ter-mapping dan data kreditur sesuai sistem OJK sebelum mengajukan.",
     "Hak Tanggungan Elektronik"),

    # ── KJKSB ────────────────────────────────────────────────
    ("Apa itu KJKSB dalam layanan pertanahan ATR/BPN?",
     "KJKSB (Kegiatan Jual-beli, Kredit, Sewa-menyewa, dan Berbagi) adalah kewajiban pelaporan transaksi pertanahan digital oleh PPAT untuk meningkatkan transparansi transaksi properti secara nasional.",
     "KJKSB"),

    ("Bagaimana cara melaporkan transaksi KJKSB di portal?",
     "Pelaporan KJKSB: (1) Login portal; (2) Menu KJKSB; (3) Pilih jenis kegiatan; (4) Isi data pihak dan objek tanah; (5) Lampirkan akta/perjanjian; (6) Submit laporan.",
     "KJKSB"),

    ("Dokumen apa saja yang diperlukan untuk pelaporan KJKSB?",
     "Dokumen KJKSB: KTP/paspor para pihak, sertifikat tanah, akta/perjanjian terkait, bukti pembayaran pajak, dan dokumen pendukung sesuai jenis kegiatan.",
     "KJKSB"),

    ("Apakah pelaporan KJKSB wajib dilakukan oleh PPAT?",
     "Ya, pelaporan KJKSB bersifat wajib bagi PPAT. Keterlambatan dapat berdampak pada catatan kepatuhan PPAT di sistem pengawasan ATR/BPN dan berpotensi dikenai sanksi administratif.",
     "KJKSB"),

    # ── KKPR Non Berusaha & Stranas ──────────────────────────
    ("Apa itu KKPR Non Berusaha?",
     "KKPR Non Berusaha adalah persetujuan pemanfaatan ruang untuk kegiatan non-komersial seperti pembangunan rumah tinggal atau fasilitas sosial oleh perorangan.",
     "KKPR Non Berusaha & Stranas"),

    ("Bagaimana cara mengajukan KKPR Non Berusaha?",
     "KKPR Non Berusaha diajukan secara daring melalui portal OSS di oss.go.id atau Dinas PTSP setempat. PPAT membantu klien menyiapkan peta bidang dan data kepemilikan tanah.",
     "KKPR Non Berusaha & Stranas"),

    ("Apa itu Stranas dalam konteks pertanahan ATR/BPN?",
     "Stranas (Strategi Nasional) adalah program prioritas pertanahan dalam Reforma Agraria yang mencakup redistribusi tanah, legalisasi aset, penyelesaian konflik agraria, dan pengakuan tanah ulayat.",
     "KKPR Non Berusaha & Stranas"),

    ("Bagaimana peran PPAT dalam program Stranas?",
     "PPAT di wilayah lokus Stranas melaporkan transaksi terkait objek redistribusi atau legalisasi aset melalui menu Laporan Stranas di portal, dan membantu masyarakat dalam proses legalisasi aset.",
     "KKPR Non Berusaha & Stranas"),
]

# ════════════════════════════════════════════════════════════
# KONTEN ARTIKEL SIDEBAR — diekstrak menjadi Q&A implisit
# agar teks penjelasan panjang ikut di-index oleh TF-IDF
# ════════════════════════════════════════════════════════════

_ARTIKEL = [
    # Akun
    ("Apa itu Portal Mitra PPAT ATR/BPN dan siapa yang bisa mengaksesnya?",
     "Portal Mitra PPAT adalah aplikasi berbasis web dari Kementerian ATR/BPN untuk mendukung tugas PPAT secara digital. Melalui portal ini PPAT dapat membuat akta, mengajukan peralihan hak, mendaftarkan Hak Tanggungan, dan melaporkan kegiatan pertanahan secara elektronik. Portal hanya bisa diakses oleh PPAT yang memiliki SK Pengangkatan aktif dari Menteri ATR/BPN.",
     "Akun, Kredensial & Autentikasi"),

    ("Bagaimana alur login pertama kali ke Portal SSO PPAT?",
     "PPAT baru mendapatkan kredensial awal (email + password sementara) dari petugas Kantor Pertanahan saat pendaftaran akun. Login pertama kali di Portal SSO menggunakan kredensial tersebut, lalu segera ganti password sesuai ketentuan keamanan portal.",
     "Akun, Kredensial & Autentikasi"),

    # Akta
    ("Bagaimana alur lengkap pembuatan akta di Portal Mitra PPAT?",
     "Alur pembuatan akta: (1) Login ke portal; (2) Pilih menu Pembuatan Akta dan tentukan jenisnya; (3) Masukkan data bidang tanah — nomor sertifikat divalidasi otomatis ke database BPN; (4) Masukkan data pihak — NIK divalidasi ke Dukcapil; (5) Periksa dan konfirmasi data; (6) Unduh draft akta PDF untuk ditandatangani.",
     "Pembuatan Akta & Validasi"),

    ("Apa perbedaan SHM, HGB, dan HGU dalam format nomor hak di portal?",
     "Jenis hak yang umum digunakan di portal: SHM (Sertifikat Hak Milik), HGB (Hak Guna Bangunan), HGU (Hak Guna Usaha), HP (Hak Pakai). Format penulisan sama: [Kode Wilayah].[Jenis Hak].[Nomor Urut]. Pastikan kode jenis hak sesuai sertifikat fisik.",
     "Pembuatan Akta & Validasi"),

    # Peralihan
    ("Apa saja jenis peralihan hak yang bisa diajukan secara elektronik?",
     "Jenis peralihan hak yang dapat diajukan elektronik melalui portal: jual beli, hibah, waris/pewarisan, tukar menukar, inbreng (pemasukan ke perusahaan), dan lelang. Masing-masing memiliki persyaratan dokumen yang berbeda sesuai ketentuan Kantor Pertanahan.",
     "Peralihan Hak Elektronik & Pembayaran"),

    ("Apa itu BPHTB dan PPh Final dalam proses peralihan hak?",
     "BPHTB (Bea Perolehan Hak atas Tanah dan Bangunan) adalah pajak yang dibayar pembeli saat menerima hak atas tanah/bangunan. PPh Final adalah pajak penghasilan yang dibayar penjual atas nilai transaksi. Keduanya wajib dilunasi sebelum akta dapat didaftarkan di Kantor Pertanahan.",
     "Peralihan Hak Elektronik & Pembayaran"),

    # Kendala
    ("Apa saja informasi yang harus disertakan saat melaporkan kendala teknis portal?",
     "Saat melapor kendala teknis, sertakan: nama lengkap dan nomor akun PPAT, deskripsi masalah secara detail, langkah-langkah yang sudah dilakukan, tangkapan layar pesan error, waktu kejadian, dan browser serta sistem operasi yang digunakan.",
     "Pelaporan Kendala Teknis"),

    # HT-el
    ("Apa perbedaan APHT dan SKMHT dalam Hak Tanggungan Elektronik?",
     "APHT (Akta Pembebanan Hak Tanggungan) adalah akta yang langsung membebankan hak tanggungan atas objek jaminan. SKMHT (Surat Kuasa Membebankan Hak Tanggungan) adalah surat kuasa dari pemilik tanah kepada kreditur untuk memasang hak tanggungan, digunakan jika APHT belum bisa langsung dibuat.",
     "Hak Tanggungan Elektronik"),

    ("Bagaimana cara menghitung PNBP untuk pendaftaran Hak Tanggungan?",
     "Biaya PNBP HT-el dihitung berdasarkan persentase dari nilai tanggungan yang tercantum dalam APHT. Besaran tarif mengacu pada Peraturan Pemerintah tentang PNBP Kementerian ATR/BPN. Portal menyediakan kalkulator PNBP otomatis — isi nilai tanggungan dan sistem akan menampilkan estimasi biaya.",
     "Hak Tanggungan Elektronik"),

    # KJKSB
    ("Kapan batas waktu pelaporan KJKSB setelah akta dibuat?",
     "Pelaporan KJKSB wajib dilakukan dalam jangka waktu yang ditentukan setelah akta ditandatangani. Keterlambatan pelaporan tercatat dalam sistem pengawasan kepatuhan PPAT dan dapat berdampak pada evaluasi kinerja PPAT oleh ATR/BPN.",
     "KJKSB"),

    # KKPR
    ("Apa perbedaan KKPR Berusaha dan KKPR Non Berusaha?",
     "KKPR Berusaha diperuntukkan bagi kegiatan usaha/komersial seperti pembangunan gedung perkantoran, mal, atau industri. KKPR Non Berusaha untuk kegiatan non-komersial seperti rumah tinggal perorangan atau fasilitas sosial. Proses pengajuan dan persyaratan keduanya berbeda.",
     "KKPR Non Berusaha & Stranas"),

    ("Apa saja program yang termasuk dalam Reforma Agraria Stranas?",
     "Program Reforma Agraria dalam Stranas ATR/BPN meliputi: (1) Redistribusi tanah — pembagian tanah negara/HGU kepada masyarakat; (2) Legalisasi aset — pensertifikatan tanah yang belum bersertifikat; (3) Penyelesaian sengketa agraria melalui mediasi; (4) Pengakuan dan perlindungan tanah ulayat masyarakat adat.",
     "KKPR Non Berusaha & Stranas"),
]

# ════════════════════════════════════════════════════════════
# Gabungkan semua data
# ════════════════════════════════════════════════════════════

_SEMUA_DATA = _QA + _ARTIKEL

_DATA = {
    "pertanyaan": [row[0] for row in _SEMUA_DATA],
    "jawaban":    [row[1] for row in _SEMUA_DATA],
    "kategori":   [row[2] for row in _SEMUA_DATA],
    "sumber":     [
        f"FAQ PPAT ATR/BPN — {row[2]}" for row in _SEMUA_DATA
    ],
}


# ════════════════════════════════════════════════════════════
# ENGINE CLASS
# ════════════════════════════════════════════════════════════

class ChatbotEngine:
    def __init__(self):
        self.df = pd.DataFrame(_DATA)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.model = LogisticRegression(max_iter=1000, class_weight="balanced")
        self._train()
        print(f"[Engine] Loaded {len(self.df)} dokumen | "
              f"{self.df['kategori'].nunique()} kategori")

    def _preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        words = [w for w in text.split() if w not in _STOP_WORDS]
        return " ".join(words)

    def _train(self):
        self.df["teks_bersih"] = self.df["pertanyaan"].apply(self._preprocess)
        X = self.df["teks_bersih"]
        y = self.df["kategori"]
        self.X_tfidf = self.vectorizer.fit_transform(X)
        self.model.fit(self.X_tfidf, y)

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

    def get_categories(self) -> list[str]:
        return sorted(self.df["kategori"].unique().tolist())

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
            "status": "berhasil",
            "pertanyaan_cocok": row["pertanyaan"],
            "jawaban":   row["jawaban"],
            "kategori":  row["kategori"],
            "sumber":    row["sumber"],
            "similarity": round(best_score, 3),
        }


# Singleton
engine = ChatbotEngine()
