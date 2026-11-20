# -*- coding: utf-8 -*-
"""Chatbot_PPAT_v2.ipynb

Chatbot FAQ PPAT — Portal Mitra Kerja Kementerian ATR/BPN
Struktur mengacu pada halaman bantuan.atrbpn.go.id

Topik yang dicakup:
  1. Akun, Kredensial & Autentikasi
  2. Pembuatan Akta & Validasi
  3. Peralihan Hak Elektronik & Pembayaran
  4. Pelaporan Kendala Teknis

Menu tambahan: Tiket Pengaduan ANDALAS, Hak Tanggungan Elektronik,
               KJKSB, KKPR Non Berusaha & Stranas
"""

# ============================================================
# Cell 1 — Instalasi library
# ============================================================

# Jalankan baris berikut jika belum terinstal:
# !pip install -q pandas numpy scikit-learn nltk ipywidgets

"""## Import Library"""

# ============================================================
# Cell 2 — Import library
# ============================================================

import pandas as pd
import numpy as np
import re
import nltk

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression

nltk.download('stopwords', quiet=True)
print("✅ Library berhasil dimuat!")

"""## Dataset FAQ PPAT ATR/BPN"""

# ============================================================
# Cell 3 — Dataset dummy sesuai struktur halaman bantuan ATR/BPN
# ============================================================

data = {
    "pertanyaan": [

        # ── 1. Akun, Kredensial & Autentikasi ─────────────────────────
        "Mengapa akun Mitra PPAT tidak bisa login ke Portal SSO?",
        "Apa penyebab akun PPAT terblokir di Portal SSO?",
        "Bagaimana cara reset password akun Portal SSO PPAT?",
        "Bagaimana cara mendaftarkan akun PPAT baru di portal mitra?",
        "Kenapa kode OTP tidak masuk ke nomor HP saat login?",
        "Bagaimana cara mengubah nomor HP yang terdaftar di akun PPAT?",

        # ── 2. Pembuatan Akta & Validasi ──────────────────────────────
        "Mengapa muncul pesan error saat membuat akta jual beli di portal?",
        "Bagaimana cara mengatasi pesan error validasi data pihak di portal?",
        "Mengapa nomor sertifikat tidak ditemukan saat validasi di sistem?",
        "Bagaimana format penulisan nomor hak yang benar di portal ATR/BPN?",
        "Bagaimana cara mencetak draft akta dari portal mitra PPAT?",
        "Apa yang harus dilakukan jika data bidang tanah tidak muncul di portal?",

        # ── 3. Peralihan Hak Elektronik & Pembayaran ──────────────────
        "Bagaimana cara mengajukan permohonan peralihan hak secara elektronik?",
        "Apa saja dokumen yang dibutuhkan untuk peralihan hak elektronik?",
        "Berapa lama proses peralihan hak elektronik di BPN?",
        "Mengapa kode billing SPS peralihan hak tidak muncul di portal?",
        "Mengapa surat pengantar berkas peralihan hak tidak bisa dicetak?",
        "Bagaimana cara mengecek status permohonan peralihan hak elektronik?",

        # ── 4. Pelaporan Kendala Teknis ───────────────────────────────
        "Ke mana PPAT harus melaporkan kendala teknis portal mitra?",
        "Bagaimana cara mengajukan tiket pengaduan melalui ANDALAS?",
        "Bagaimana cara menghubungi helpdesk ATR/BPN untuk kendala portal?",
        "Apakah tersedia panduan pengguna portal mitra PPAT?",

        # ── 5. Hak Tanggungan Elektronik ──────────────────────────────
        "Apa itu Hak Tanggungan Elektronik di portal ATR/BPN?",
        "Bagaimana cara mendaftarkan Hak Tanggungan secara elektronik?",
        "Berapa biaya pendaftaran Hak Tanggungan Elektronik?",
        "Mengapa APHT tidak bisa diajukan secara elektronik?",

        # ── 6. KJKSB ──────────────────────────────────────────────────
        "Apa itu KJKSB dalam layanan pertanahan ATR/BPN?",
        "Bagaimana cara mengakses layanan KJKSB melalui portal?",
        "Dokumen apa saja yang diperlukan untuk permohonan KJKSB?",

        # ── 7. KKPR Non Berusaha & Stranas ────────────────────────────
        "Apa itu KKPR Non Berusaha dalam layanan ATR/BPN?",
        "Bagaimana cara mengajukan permohonan KKPR Non Berusaha?",
        "Apa itu Stranas dalam konteks layanan pertanahan?",
        "Bagaimana cara PPAT mendukung program Stranas di portal?"

    ],

    "jawaban": [

        # ── 1. Akun, Kredensial & Autentikasi ─────────────────────────
        "Akun Mitra PPAT tidak bisa login ke Portal SSO umumnya disebabkan oleh: (1) Masa berlaku SK Pengangkatan/Perpanjangan sudah habis; (2) Data PPAT belum diperbarui di sistem Ditjen Penetapan Hak dan Pendaftaran Tanah; (3) Password salah atau akun terkunci. Pastikan SK masih aktif dan data sudah diperbarui oleh Kantor Pertanahan setempat.",
        "Akun PPAT dapat terblokir jika terjadi percobaan login yang gagal berulang kali (lebih dari 5 kali), atau jika sistem mendeteksi aktivitas mencurigakan. Tunggu 30 menit lalu coba lagi, atau ajukan pembukaan blokir melalui Helpdesk ATR/BPN.",
        "Reset password dapat dilakukan di halaman login Portal SSO dengan mengklik tombol 'Lupa Password'. Masukkan alamat email terdaftar, lalu ikuti tautan yang dikirimkan ke email tersebut. Tautan berlaku selama 24 jam.",
        "Pendaftaran akun PPAT baru dilakukan melalui Kantor Pertanahan setempat. PPAT membawa SK Pengangkatan asli beserta dokumen pendukung. Petugas akan mendaftarkan akun ke sistem SSO dan mengirimkan kredensial awal ke email resmi PPAT.",
        "Kode OTP tidak masuk dapat disebabkan: nomor HP tidak terdaftar di sistem, gangguan jaringan provider, atau delay pengiriman SMS. Klik 'Kirim Ulang OTP' setelah 60 detik. Jika masalah berlanjut, hubungi Helpdesk untuk memverifikasi nomor HP terdaftar.",
        "Perubahan nomor HP terdaftar di akun PPAT harus dilakukan melalui Kantor Pertanahan setempat dengan membawa identitas diri dan SK PPAT. Petugas akan memperbarui data di sistem SSO.",

        # ── 2. Pembuatan Akta & Validasi ──────────────────────────────
        "Pesan error saat membuat akta jual beli umumnya terjadi karena: (1) Data bidang tanah belum lengkap atau NIK pihak tidak valid di database Dukcapil; (2) Sesi login sudah habis (timeout); (3) Format input tidak sesuai. Lakukan logout lalu login kembali, periksa kelengkapan data, dan pastikan NIK sesuai KTP aktif.",
        "Error validasi data pihak biasanya disebabkan NIK tidak terdaftar di Dukcapil atau terdapat ketidaksesuaian nama. Pastikan NIK diinput dengan benar dan sesuai KTP. Jika NIK valid namun tetap error, laporkan ke Helpdesk disertai tangkapan layar pesan error.",
        "Nomor sertifikat tidak ditemukan di sistem dapat berarti: (1) Data belum ter-digitasi; (2) Sertifikat diterbitkan oleh kantor pertanahan lain; (3) Terdapat kesalahan penulisan nomor. Konfirmasi kebenaran nomor dan wilayah ke Kantor Pertanahan penerbit sertifikat.",
        "Format nomor hak yang benar mengikuti pola: [Kode Kabupaten/Kota].[Kode Kecamatan].[Jenis Hak].[Nomor Urut], contoh: 3273.010.SHM.00123. Pastikan tidak ada spasi, titik tambahan, atau karakter khusus. Ikuti panduan format yang tersedia di menu Bantuan portal.",
        "Untuk mencetak draft akta, buka menu 'Daftar Akta', pilih akta yang dimaksud, lalu klik tombol 'Unduh Draft PDF'. Pastikan browser mengizinkan pop-up dari domain portal. Gunakan browser Chrome atau Firefox versi terbaru untuk hasil optimal.",
        "Jika data bidang tanah tidak muncul, kemungkinan data bidang belum terpetakan ke wilayah kerja PPAT, atau terdapat kesalahan kode wilayah. Hubungi petugas Kantor Pertanahan untuk memastikan bidang tanah telah terdaftar dan terpetakan dengan benar.",

        # ── 3. Peralihan Hak Elektronik & Pembayaran ──────────────────
        "Pengajuan peralihan hak elektronik dilakukan melalui: (1) Login ke portal mitra PPAT; (2) Pilih menu 'Layanan Elektronik' → 'Peralihan Hak'; (3) Isi formulir permohonan dan unggah dokumen persyaratan; (4) Bayar kode billing yang dihasilkan sistem; (5) Pantau status melalui menu Tracking Permohonan.",
        "Dokumen persyaratan peralihan hak elektronik meliputi: sertifikat asli, akta PPAT terkait, KTP seluruh pihak, bukti pembayaran BPHTB dan PPh Final, surat pernyataan sesuai jenis peralihan, serta dokumen pendukung lain sesuai ketentuan Kantor Pertanahan setempat.",
        "Proses peralihan hak elektronik umumnya diselesaikan dalam 5–7 hari kerja setelah berkas dinyatakan lengkap dan valid oleh petugas Kantor Pertanahan. Waktu dapat berbeda tergantung antrean dan kebijakan masing-masing Kantor Pertanahan.",
        "Kode billing SPS tidak muncul biasanya karena: (1) Data formulir permohonan belum lengkap atau masih berstatus draft; (2) Sistem SPS sedang dalam pemeliharaan. Pastikan semua field wajib terisi, simpan permohonan, lalu muat ulang halaman. Jika masalah berlanjut, hubungi Helpdesk.",
        "Surat pengantar berkas yang tidak bisa dicetak dapat disebabkan status permohonan belum diverifikasi oleh petugas, atau koneksi internet tidak stabil saat proses generate dokumen. Periksa status permohonan di menu Tracking, lalu coba cetak ulang setelah status berubah menjadi 'Siap Cetak'.",
        "Status permohonan peralihan hak dapat dipantau melalui menu 'Tracking Permohonan' di portal dengan memasukkan nomor berkas yang diperoleh saat pendaftaran. Notifikasi perubahan status juga dikirimkan melalui email terdaftar.",

        # ── 4. Pelaporan Kendala Teknis ───────────────────────────────
        "Kendala teknis portal PPAT dapat dilaporkan melalui: (1) Fitur Tiket Pengaduan ANDALAS di portal; (2) Email helpdesk@atrbpn.go.id; (3) Call Center Kementerian ATR/BPN; (4) Media sosial resmi @kementerian_atrbpn. Sertakan tangkapan layar dan deskripsi langkah yang sudah dilakukan saat melapor.",
        "Tiket pengaduan ANDALAS diajukan melalui menu 'Tiket Pengaduan' di portal. Pilih kategori masalah yang sesuai, deskripsikan kendala secara detail, lampirkan tangkapan layar jika ada, lalu klik Kirim. Nomor tiket akan dikirimkan ke email untuk keperluan pemantauan.",
        "Helpdesk ATR/BPN dapat dihubungi melalui portal Sentuh Tanahku, email helpdesk@atrbpn.go.id, atau melalui halaman Pusat Kontak & Bantuan di bantuan.atrbpn.go.id. Jam layanan Helpdesk adalah Senin–Jumat pukul 08.00–16.00 WIB.",
        "Panduan pengguna portal Mitra PPAT tersedia di menu 'Bantuan' → 'Unduh Panduan' di portal. Panduan juga dapat diakses melalui halaman bantuan.atrbpn.go.id pada bagian Tanya Jawab (FAQ) dan artikel panduan teknis.",

        # ── 5. Hak Tanggungan Elektronik ──────────────────────────────
        "Hak Tanggungan Elektronik (HT-el) adalah layanan pendaftaran hak tanggungan secara daring yang diintegrasikan dalam Portal Mitra ATR/BPN. Layanan ini memungkinkan PPAT mendaftarkan Akta Pembebanan Hak Tanggungan (APHT) dan Surat Kuasa Membebankan Hak Tanggungan (SKMHT) tanpa harus datang ke kantor pertanahan.",
        "Pendaftaran Hak Tanggungan Elektronik dilakukan melalui: (1) Login portal mitra PPAT; (2) Pilih menu 'Hak Tanggungan Elektronik'; (3) Isi data debitur, kreditur, dan objek jaminan; (4) Unggah APHT dan dokumen pendukung; (5) Bayar PNBP melalui kode billing yang digenerate sistem; (6) Pantau status pendaftaran.",
        "Biaya PNBP pendaftaran Hak Tanggungan Elektronik dihitung berdasarkan nilai tanggungan sesuai Peraturan Pemerintah tentang PNBP Kementerian ATR/BPN. Rincian tarif dapat dilihat di kalkulator PNBP yang tersedia di portal sebelum melakukan pembayaran.",
        "APHT tidak bisa diajukan secara elektronik biasanya karena: (1) Data sertifikat belum ter-mapping di sistem HT-el; (2) PPAT belum terdaftar sebagai pengguna layanan HT-el; (3) Terdapat ketidaksesuaian data kreditur dengan sistem OJK. Hubungi Kantor Pertanahan untuk aktivasi akses HT-el.",

        # ── 6. KJKSB ──────────────────────────────────────────────────
        "KJKSB (Kegiatan Jual-beli, Kredit, Sewa-menyewa, dan Berbagi) adalah layanan pencatatan transaksi pertanahan berbasis digital di portal ATR/BPN yang bertujuan meningkatkan transparansi dan pengawasan transaksi properti di Indonesia.",
        "Layanan KJKSB dapat diakses melalui menu 'KJKSB' di portal mitra PPAT setelah PPAT login menggunakan akun SSO. Pilih jenis transaksi yang sesuai, isi data pihak dan objek tanah, lalu ikuti alur pengisian yang tersedia.",
        "Dokumen yang diperlukan untuk permohonan KJKSB meliputi: identitas para pihak (KTP/Paspor), dokumen kepemilikan tanah (sertifikat), akta/perjanjian terkait transaksi, bukti pembayaran pajak terkait, serta dokumen pendukung sesuai jenis kegiatan.",

        # ── 7. KKPR Non Berusaha & Stranas ────────────────────────────
        "KKPR Non Berusaha (Kesesuaian Kegiatan Pemanfaatan Ruang untuk Non Usaha) adalah persetujuan pemanfaatan ruang yang diperuntukkan bagi kegiatan yang tidak bersifat komersial, seperti pembangunan rumah tinggal atau fasilitas sosial oleh perorangan.",
        "Permohonan KKPR Non Berusaha diajukan secara daring melalui portal OSS (Online Single Submission) di oss.go.id atau melalui dinas terkait. PPAT dapat membantu klien dalam mempersiapkan dokumen persyaratan teknis seperti peta bidang dan data kepemilikan tanah.",
        "Stranas (Strategi Nasional) dalam konteks pertanahan merujuk pada program prioritas nasional bidang pertanahan yang meliputi redistribusi tanah, legalisasi aset, dan penyelesaian konflik agraria sebagai bagian dari Reforma Agraria yang dikoordinasikan Kementerian ATR/BPN.",
        "PPAT dapat mendukung program Stranas melalui portal dengan melaporkan transaksi pertanahan yang terkait objek redistribusi atau legalisasi aset, menggunakan menu 'Laporan Stranas' yang tersedia bagi PPAT yang wilayah kerjanya masuk dalam lokus program Stranas."

    ],

    "kategori": [
        # Akun & Autentikasi (6)
        "Akun, Kredensial & Autentikasi",
        "Akun, Kredensial & Autentikasi",
        "Akun, Kredensial & Autentikasi",
        "Akun, Kredensial & Autentikasi",
        "Akun, Kredensial & Autentikasi",
        "Akun, Kredensial & Autentikasi",
        # Pembuatan Akta (6)
        "Pembuatan Akta & Validasi",
        "Pembuatan Akta & Validasi",
        "Pembuatan Akta & Validasi",
        "Pembuatan Akta & Validasi",
        "Pembuatan Akta & Validasi",
        "Pembuatan Akta & Validasi",
        # Peralihan Hak (6)
        "Peralihan Hak Elektronik & Pembayaran",
        "Peralihan Hak Elektronik & Pembayaran",
        "Peralihan Hak Elektronik & Pembayaran",
        "Peralihan Hak Elektronik & Pembayaran",
        "Peralihan Hak Elektronik & Pembayaran",
        "Peralihan Hak Elektronik & Pembayaran",
        # Kendala Teknis (4)
        "Pelaporan Kendala Teknis",
        "Pelaporan Kendala Teknis",
        "Pelaporan Kendala Teknis",
        "Pelaporan Kendala Teknis",
        # HT-el (4)
        "Hak Tanggungan Elektronik",
        "Hak Tanggungan Elektronik",
        "Hak Tanggungan Elektronik",
        "Hak Tanggungan Elektronik",
        # KJKSB (3)
        "KJKSB",
        "KJKSB",
        "KJKSB",
        # KKPR & Stranas (4)
        "KKPR Non Berusaha & Stranas",
        "KKPR Non Berusaha & Stranas",
        "KKPR Non Berusaha & Stranas",
        "KKPR Non Berusaha & Stranas",
    ],

    "sumber": [
        "FAQ PPAT ATR/BPN — Akun, Kredensial & Autentikasi",
        "FAQ PPAT ATR/BPN — Akun, Kredensial & Autentikasi",
        "FAQ PPAT ATR/BPN — Akun, Kredensial & Autentikasi",
        "FAQ PPAT ATR/BPN — Akun, Kredensial & Autentikasi",
        "FAQ PPAT ATR/BPN — Akun, Kredensial & Autentikasi",
        "FAQ PPAT ATR/BPN — Akun, Kredensial & Autentikasi",
        "FAQ PPAT ATR/BPN — Pembuatan Akta & Validasi",
        "FAQ PPAT ATR/BPN — Pembuatan Akta & Validasi",
        "FAQ PPAT ATR/BPN — Pembuatan Akta & Validasi",
        "FAQ PPAT ATR/BPN — Pembuatan Akta & Validasi",
        "FAQ PPAT ATR/BPN — Pembuatan Akta & Validasi",
        "FAQ PPAT ATR/BPN — Pembuatan Akta & Validasi",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik & Pembayaran",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik & Pembayaran",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik & Pembayaran",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik & Pembayaran",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik & Pembayaran",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik & Pembayaran",
        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis",
        "FAQ PPAT ATR/BPN — Tiket Pengaduan ANDALAS",
        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis",
        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis",
        "FAQ PPAT ATR/BPN — Hak Tanggungan Elektronik",
        "FAQ PPAT ATR/BPN — Hak Tanggungan Elektronik",
        "FAQ PPAT ATR/BPN — Hak Tanggungan Elektronik",
        "FAQ PPAT ATR/BPN — Hak Tanggungan Elektronik",
        "FAQ PPAT ATR/BPN — KJKSB",
        "FAQ PPAT ATR/BPN — KJKSB",
        "FAQ PPAT ATR/BPN — KJKSB",
        "FAQ PPAT ATR/BPN — KKPR Non Berusaha & Stranas",
        "FAQ PPAT ATR/BPN — KKPR Non Berusaha & Stranas",
        "FAQ PPAT ATR/BPN — KKPR Non Berusaha & Stranas",
        "FAQ PPAT ATR/BPN — KKPR Non Berusaha & Stranas",
    ]
}

df = pd.DataFrame(data)
print(f"Dataset dimuat: {len(df)} pertanyaan, {df['kategori'].nunique()} kategori")
df.head()

"""## Preprocessing Teks"""

# ============================================================
# Cell 4 — Preprocessing
# ============================================================

stop_words = set(stopwords.words('indonesian'))

def preprocessing(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

df["pertanyaan_bersih"] = df["pertanyaan"].apply(preprocessing)
df[["pertanyaan", "pertanyaan_bersih"]].head(5)

"""## Training Model"""

# ============================================================
# Cell 5 — Training model klasifikasi kategori
# ============================================================

X = df["pertanyaan_bersih"]
y = df["kategori"]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_tfidf = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_tfidf, y)

print("✅ Training selesai!")
print(f"   Jumlah data   : {len(df)}")
print(f"   Jumlah kategori: {df['kategori'].nunique()}")
print(f"   Kategori: {list(df['kategori'].unique())}")

"""## Fungsi Pencarian Jawaban"""

# ============================================================
# Cell 6 — Mesin pencari jawaban dengan cosine similarity
# ============================================================

def cari_jawaban(pertanyaan):
    pertanyaan_bersih = preprocessing(pertanyaan)
    query_vector = vectorizer.transform([pertanyaan_bersih])

    # Prediksi kategori terdekat
    kategori = model.predict(query_vector)[0]

    # Filter data pada kategori tersebut
    data_kategori = df[df["kategori"] == kategori]
    kategori_vectors = vectorizer.transform(data_kategori["pertanyaan_bersih"])

    # Hitung similarity dalam kategori
    scores = cosine_similarity(query_vector, kategori_vectors)[0]
    best_index = np.argmax(scores)
    similarity = scores[best_index]

    # Jika similarity terlalu rendah → tampilkan rekomendasi
    if similarity < 0.20:
        semua_vectors = vectorizer.transform(df["pertanyaan_bersih"])
        semua_scores = cosine_similarity(query_vector, semua_vectors)[0]
        top_indices = np.argsort(semua_scores)[::-1][:3]

        rekomendasi = [df.iloc[i]["pertanyaan"] for i in top_indices if semua_scores[i] > 0.0]
        if not rekomendasi:
            rekomendasi = df["pertanyaan"].sample(3).tolist()

        return {
            "status": "Tidak ditemukan",
            "jawaban": "Maaf, saya belum memiliki informasi terkait pertanyaan tersebut. Silakan hubungi Helpdesk ATR/BPN.",
            "kategori": kategori,
            "similarity": round(float(similarity), 3),
            "rekomendasi": rekomendasi
        }

    hasil = data_kategori.iloc[best_index]
    return {
        "status": "Berhasil",
        "kategori": kategori,
        "pertanyaan": hasil["pertanyaan"],
        "jawaban": hasil["jawaban"],
        "sumber": hasil["sumber"],
        "similarity": round(float(similarity), 3)
    }

"""## Uji Coba Pertanyaan"""

# ============================================================
# Cell 7 — Uji coba dengan pertanyaan sampel dari tiap kategori
# ============================================================

pertanyaan_uji = [
    "Kenapa akun PPAT saya tidak bisa masuk ke portal SSO?",
    "Muncul error saat bikin akta, apa yang harus dilakukan?",
    "Kode billing peralihan hak tidak keluar, kenapa?",
    "Surat pengantar tidak bisa dicetak bagaimana solusinya?",
    "Cara daftar Hak Tanggungan lewat portal?",
    "Apa itu KJKSB di portal ATR/BPN?",
    "Bagaimana mengajukan KKPR untuk rumah tinggal?",
    "Ke mana lapor kalau portal error?"
]

for q in pertanyaan_uji:
    hasil = cari_jawaban(q)
    print("─" * 60)
    print(f"❓ Pertanyaan : {q}")
    print(f"📂 Kategori   : {hasil['kategori']}")
    print(f"💬 Jawaban    : {hasil['jawaban'][:120]}...")
    print(f"🎯 Similarity : {hasil['similarity']}")

"""## Fungsi Tambah Pengetahuan"""

# ============================================================
# Cell 8 — Tambah data dan retrain model
# ============================================================

def tambah_pengetahuan(pertanyaan_baru, jawaban_baru, kategori_baru, sumber_baru):
    global df, vectorizer, model, X_tfidf

    new_row = pd.DataFrame({
        "pertanyaan": [pertanyaan_baru],
        "jawaban": [jawaban_baru],
        "kategori": [kategori_baru],
        "sumber": [sumber_baru],
        "pertanyaan_bersih": [preprocessing(pertanyaan_baru)]
    })

    df = pd.concat([df, new_row], ignore_index=True)

    X = df["pertanyaan_bersih"]
    y = df["kategori"]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_tfidf = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_tfidf, y)

    print(f"✅ Data baru ditambahkan. Total database: {len(df)} pertanyaan.")

# Contoh penambahan topik baru: Sentuh Tanahku
tambah_pengetahuan(
    pertanyaan_baru="Bagaimana cara menggunakan aplikasi Sentuh Tanahku?",
    jawaban_baru="Aplikasi Sentuh Tanahku dapat diunduh di Google Play Store atau App Store. Setelah instal, daftarkan akun menggunakan NIK dan nomor sertifikat untuk mengecek informasi bidang tanah, riwayat sertipikat, dan layanan pertanahan lainnya secara mandiri.",
    kategori_baru="Pelaporan Kendala Teknis",
    sumber_baru="FAQ PPAT ATR/BPN — Sentuh Tanahku"
)

# Langsung uji
hasil_tes = cari_jawaban("cara pakai aplikasi Sentuh Tanahku")
print(f"\n❓ Pertanyaan : cara pakai aplikasi Sentuh Tanahku")
print(f"💬 Jawaban    : {hasil_tes['jawaban'][:150]}...")
print(f"📌 Sumber     : {hasil_tes.get('sumber', '-')}")

"""## Chatbot Interaktif (Widget UI)"""

# ============================================================
# Cell 9 — UI Chatbot interaktif sesuai tampilan bantuan ATR/BPN
# ============================================================

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# ── Warna tema ATR/BPN ──────────────────────────────────────
WARNA_HEADER   = "#C0392B"   # Merah ATR/BPN
WARNA_USER     = "#FDECEA"   # Bubble user
WARNA_BOT_OK   = "#EBF5FB"   # Bubble bot — jawaban ditemukan
WARNA_BOT_FAIL = "#FEF9E7"   # Bubble bot — tidak ditemukan
BORDER_BOT_OK  = "#2980B9"
BORDER_BOT_FAIL= "#E67E22"

# ── Widget ──────────────────────────────────────────────────
input_pertanyaan = widgets.Text(
    value='',
    placeholder='Tulis pertanyaan seputar portal PPAT ATR/BPN...',
    description='',
    layout=widgets.Layout(width='75%', height='36px')
)

tombol_kirim = widgets.Button(
    description='Kirim',
    button_style='danger',
    tooltip='Klik untuk mendapatkan jawaban',
    layout=widgets.Layout(width='12%', height='36px')
)

output_chat = widgets.Output(
    layout=widgets.Layout(
        min_height='300px',
        max_height='500px',
        overflow_y='auto',
        border='1px solid #ddd',
        padding='10px',
        border_radius='8px'
    )
)

def proses_tanya(pertanyaan):
    with output_chat:

        # Bubble pertanyaan pengguna
        display(HTML(f'''
        <div style="background:{WARNA_USER};padding:10px 14px;border-radius:12px 12px 2px 12px;
                    margin:6px 0 6px 20%;border:1px solid #FADBD8;font-size:14px;">
            <b style="color:#922B21;">👤 Anda:</b><br>{pertanyaan}
        </div>
        '''))

        hasil = cari_jawaban(pertanyaan)

        if hasil["status"] == "Berhasil":
            display(HTML(f'''
            <div style="background:{WARNA_BOT_OK};padding:12px 14px;border-radius:12px 12px 12px 2px;
                        margin:6px 20% 6px 0;border-left:4px solid {BORDER_BOT_OK};font-size:14px;">
                <b style="color:#1A5276;">🤖 BPN-Bot:</b><br><br>
                {hasil["jawaban"]}<br><br>
                <hr style="border:none;border-top:1px solid #D6EAF8;margin:8px 0;">
                <small style="color:#626567;">
                    📂 <b>Kategori:</b> {hasil["kategori"]} &nbsp;|&nbsp;
                    🎯 <b>Relevansi:</b> {hasil["similarity"]}<br>
                    📌 <b>Sumber:</b> {hasil.get("sumber", "-")}
                </small>
            </div>
            '''))
        else:
            opsi = "".join([
                f'<li style="margin-bottom:5px;color:#1A5276;cursor:pointer;">'
                f'<b>"{rec}"</b></li>'
                for rec in hasil["rekomendasi"]
            ])
            display(HTML(f'''
            <div style="background:{WARNA_BOT_FAIL};padding:12px 14px;border-radius:12px 12px 12px 2px;
                        margin:6px 20% 6px 0;border-left:4px solid {BORDER_BOT_FAIL};font-size:14px;">
                <b style="color:#784212;">🤖 BPN-Bot:</b><br><br>
                {hasil["jawaban"]}<br><br>
                <b>Mungkin Anda ingin menanyakan:</b>
                <ul style="margin-top:6px;padding-left:20px;">{opsi}</ul>
                <small style="color:#777;">
                    💡 Salin salah satu pertanyaan di atas ke kolom input, atau hubungi
                    <b>Helpdesk ATR/BPN</b> untuk bantuan langsung.
                </small>
            </div>
            '''))

def tangani_kirim(sender):
    pertanyaan = input_pertanyaan.value.strip()
    if not pertanyaan:
        return
    proses_tanya(pertanyaan)
    input_pertanyaan.value = ''

tombol_kirim.on_click(tangani_kirim)
input_pertanyaan.on_submit(tangani_kirim)

# ── Layout utama ─────────────────────────────────────────────
header = widgets.HTML(f'''
<div style="background:{WARNA_HEADER};color:white;padding:14px 18px;
            border-radius:8px 8px 0 0;margin-bottom:0;">
    <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-size:22px;">🏛️</span>
        <div>
            <b style="font-size:16px;">BPN-Bot — Asisten FAQ Portal PPAT</b><br>
            <small style="opacity:0.85;">Kementerian Agraria dan Tata Ruang / Badan Pertanahan Nasional</small>
        </div>
    </div>
</div>
<div style="background:#F9EBEA;padding:8px 14px;border:1px solid #FADBD8;
            border-radius:0;font-size:12px;color:#922B21;">
    📋 Topik: Akun SSO · Pembuatan Akta · Peralihan Hak · HT-el · KJKSB · KKPR · ANDALAS · Stranas
</div>
''')

input_area = widgets.HBox(
    [input_pertanyaan, tombol_kirim],
    layout=widgets.Layout(margin='10px 0 6px 0', gap='8px')
)

ui = widgets.VBox(
    [header, input_area, output_chat],
    layout=widgets.Layout(
        width='100%',
        max_width='860px',
        border='1px solid #E5E7E9',
        border_radius='8px',
        padding='12px'
    )
)

display(ui)
