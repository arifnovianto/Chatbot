# -*- coding: utf-8 -*-
"""Chatbot_PPAT.ipynb

Chatbot FAQ PPAT - Portal Mitra Kerja Kementerian ATR/BPN
Dibuat sebagai dummy untuk keperluan pengembangan & demo.
"""

# ============================================================
# Cell 1 — Instalasi library
# ============================================================

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

nltk.download('stopwords')

print("Library berhasil dimuat!")

"""## Dataset FAQ PPAT ATR/BPN"""

# ============================================================
# Cell 3 — Dataset dummy FAQ PPAT
# ============================================================

data = {
    "pertanyaan": [
        # Akun & Autentikasi
        "Mengapa akun Mitra PPAT tidak bisa login ke Portal SSO?",
        "Bagaimana cara reset password akun PPAT?",
        "Apa yang harus dilakukan jika akun PPAT terkunci?",
        "Bagaimana cara mendaftarkan akun PPAT baru di portal?",
        "Kenapa kode OTP tidak masuk saat login?",

        # Pembuatan Akta & Validasi
        "Mengapa muncul pesan error saat membuat akta jual beli?",
        "Bagaimana cara validasi nomor sertifikat di sistem?",
        "Mengapa nomor sertifikat tidak ditemukan di database?",
        "Apa format penulisan nomor hak yang benar di portal?",
        "Bagaimana cara mencetak draft akta dari portal?",

        # Peralihan Hak Elektronik
        "Bagaimana cara mengajukan peralihan hak secara elektronik?",
        "Apa saja dokumen yang dibutuhkan untuk peralihan hak elektronik?",
        "Berapa lama proses peralihan hak elektronik di BPN?",
        "Mengapa kode billing SPS peralihan hak tidak muncul?",
        "Bagaimana cara mengecek status permohonan peralihan hak?",

        # Pelaporan & Kendala Teknis
        "Ke mana PPAT harus melaporkan kendala teknis portal?",
        "Bagaimana cara menghubungi helpdesk ATR/BPN?",
        "Apa nomor kontak pusat bantuan Kementerian ATR/BPN?",
        "Bagaimana cara mengajukan tiket pengaduan ANDALAS?",
        "Apakah ada panduan pengguna portal mitra PPAT?"
    ],

    "jawaban": [
        # Akun & Autentikasi
        "Akun Mitra PPAT tidak bisa login biasanya disebabkan masa berlaku SK Pengangkatan yang sudah habis, data belum diperbarui di sistem Ditjen Penetapan Hak, atau password salah. Pastikan SK masih aktif dan hubungi Kantor Pertanahan setempat jika diperlukan.",
        "Reset password dapat dilakukan melalui halaman login Portal SSO dengan mengklik 'Lupa Password', lalu masukkan email terdaftar. Tautan reset akan dikirimkan ke email tersebut.",
        "Jika akun terkunci akibat percobaan login berulang, tunggu 30 menit lalu coba kembali. Jika masih terkunci, ajukan permohonan buka kunci melalui Helpdesk ATR/BPN.",
        "Pendaftaran akun PPAT baru dilakukan melalui Kantor Pertanahan setempat dengan membawa SK Pengangkatan asli. Petugas akan mendaftarkan akun ke sistem dan mengirimkan kredensial awal.",
        "Kode OTP tidak masuk bisa disebabkan nomor HP tidak terdaftar, sinyal buruk, atau delay provider. Coba klik 'Kirim Ulang OTP' setelah 60 detik, atau hubungi Helpdesk jika masalah berlanjut.",

        # Pembuatan Akta & Validasi
        "Error saat membuat akta jual beli umumnya terjadi karena data bidang tanah belum lengkap, NIK penjual/pembeli tidak valid di Dukcapil, atau sesi login sudah habis. Logout lalu login kembali dan periksa kelengkapan data.",
        "Validasi nomor sertifikat dilakukan pada menu 'Pengecekan Sertifikat' di portal. Masukkan nomor hak dan kode wilayah dengan benar, lalu klik Cek. Pastikan format nomor sesuai ketentuan.",
        "Nomor sertifikat tidak ditemukan bisa berarti data belum ter-digitasi, sertifikat berasal dari kantor pertanahan lain, atau terdapat kesalahan penulisan. Konfirmasi ke Kantor Pertanahan penerbit sertifikat.",
        "Format penulisan nomor hak yang benar adalah kode provinsi-kode kabupaten-kode kecamatan-nomor urut, contoh: 32.73.01.00001. Pastikan tidak ada spasi atau karakter khusus.",
        "Untuk mencetak draft akta, buka menu 'Daftar Akta', pilih akta yang dimaksud, lalu klik tombol 'Unduh Draft PDF'. Pastikan browser mengizinkan pop-up dari portal.",

        # Peralihan Hak Elektronik
        "Pengajuan peralihan hak elektronik dilakukan melalui menu 'Layanan Elektronik' → 'Peralihan Hak'. Isi formulir, unggah dokumen persyaratan, dan bayar kode billing yang dihasilkan sistem.",
        "Dokumen yang dibutuhkan untuk peralihan hak elektronik meliputi: sertifikat asli, akta PPAT, KTP para pihak, bukti pembayaran BPHTB dan PPh, serta surat pernyataan yang diperlukan sesuai jenis peralihan.",
        "Proses peralihan hak elektronik umumnya memakan waktu 5–7 hari kerja setelah berkas dinyatakan lengkap dan valid oleh Kantor Pertanahan.",
        "Kode billing SPS tidak muncul biasanya karena data permohonan belum lengkap atau sistem sedang maintenance. Periksa notifikasi sistem dan coba kembali beberapa saat, atau hubungi Helpdesk.",
        "Status permohonan peralihan hak dapat dicek melalui menu 'Tracking Permohonan' di portal dengan memasukkan nomor berkas yang diperoleh saat pendaftaran.",

        # Pelaporan & Kendala Teknis
        "Kendala teknis portal PPAT dapat dilaporkan melalui fitur Tiket Pengaduan ANDALAS di portal, melalui email helpdesk, atau menghubungi Call Center Kementerian ATR/BPN.",
        "Helpdesk ATR/BPN dapat dihubungi melalui portal Sentuh Tanahku, email: helpdesk@atrbpn.go.id, atau melalui media sosial resmi Kementerian ATR/BPN.",
        "Nomor kontak pusat bantuan Kementerian ATR/BPN dapat ditemukan di halaman resmi www.atrbpn.go.id pada menu Hubungi Kami atau melalui aplikasi Sentuh Tanahku.",
        "Tiket pengaduan ANDALAS diajukan melalui menu 'Tiket Pengaduan' di portal, pilih kategori masalah, deskripsikan kendala secara detail, dan lampirkan tangkapan layar jika ada.",
        "Panduan pengguna portal Mitra PPAT tersedia di menu 'Bantuan' → 'Unduh Panduan' di portal, atau dapat diakses melalui halaman Bantuan ATR/BPN di bantuan.atrbpn.go.id."
    ],

    "kategori": [
        "Akun & Autentikasi", "Akun & Autentikasi", "Akun & Autentikasi",
        "Akun & Autentikasi", "Akun & Autentikasi",

        "Pembuatan Akta & Validasi", "Pembuatan Akta & Validasi", "Pembuatan Akta & Validasi",
        "Pembuatan Akta & Validasi", "Pembuatan Akta & Validasi",

        "Peralihan Hak Elektronik", "Peralihan Hak Elektronik", "Peralihan Hak Elektronik",
        "Peralihan Hak Elektronik", "Peralihan Hak Elektronik",

        "Pelaporan & Kendala Teknis", "Pelaporan & Kendala Teknis", "Pelaporan & Kendala Teknis",
        "Pelaporan & Kendala Teknis", "Pelaporan & Kendala Teknis"
    ],

    "sumber": [
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

        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik",
        "FAQ PPAT ATR/BPN — Peralihan Hak Elektronik",

        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis",
        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis",
        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis",
        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis",
        "FAQ PPAT ATR/BPN — Pelaporan Kendala Teknis"
    ]
}

df = pd.DataFrame(data)
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
df[["pertanyaan", "pertanyaan_bersih"]].head()

"""## Training Model Klasifikasi"""

# ============================================================
# Cell 5 — Training model
# ============================================================

X = df["pertanyaan_bersih"]
y = df["kategori"]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_tfidf = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_tfidf, y)

print("Training model berhasil!")
print(f"Total data: {len(df)} pertanyaan | Kategori: {df['kategori'].nunique()}")

"""## Fungsi Pencarian Jawaban"""

# ============================================================
# Cell 6 — Fungsi pencarian jawaban
# ============================================================

def cari_jawaban(pertanyaan):
    pertanyaan_bersih = preprocessing(pertanyaan)
    query_vector = vectorizer.transform([pertanyaan_bersih])

    # Prediksi kategori
    kategori = model.predict(query_vector)[0]

    # Filter data berdasarkan kategori
    data_kategori = df[df["kategori"] == kategori]
    kategori_vectors = vectorizer.transform(data_kategori["pertanyaan_bersih"])

    # Hitung cosine similarity
    scores = cosine_similarity(query_vector, kategori_vectors)[0]
    best_index = np.argmax(scores)
    similarity = scores[best_index]

    if similarity < 0.25:
        # Cari rekomendasi dari seluruh database
        semua_vectors = vectorizer.transform(df["pertanyaan_bersih"])
        semua_scores = cosine_similarity(query_vector, semua_vectors)[0]
        top_indices = np.argsort(semua_scores)[::-1][:3]

        rekomendasi = [df.iloc[i]["pertanyaan"] for i in top_indices if semua_scores[i] > 0.0]
        if not rekomendasi:
            rekomendasi = df["pertanyaan"].sample(3).tolist()

        return {
            "status": "Tidak ditemukan",
            "jawaban": "Maaf, saya belum memiliki informasi terkait pertanyaan tersebut.",
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
# Cell 7 — Uji coba
# ============================================================

pertanyaan_uji = [
    "Kenapa akun PPAT saya tidak bisa masuk portal?",
    "Dokumen apa saja yang perlu disiapkan untuk peralihan hak?",
    "Bagaimana cara melaporkan error di portal?",
    "Nomor sertifikat tidak terbaca di sistem, kenapa?"
]

for q in pertanyaan_uji:
    hasil = cari_jawaban(q)
    print(f"\nPertanyaan : {q}")
    print(f"Kategori   : {hasil['kategori']}")
    print(f"Jawaban    : {hasil['jawaban']}")
    print(f"Similarity : {hasil['similarity']}")

"""## Fungsi Tambah Pengetahuan"""

# ============================================================
# Cell 8 — Tambah data baru & retrain
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

    print(f"Data baru ditambahkan. Total database: {len(df)} pertanyaan.")

# Contoh penambahan data baru
tambah_pengetahuan(
    pertanyaan_baru="Bagaimana cara mengunduh sertifikat elektronik dari portal?",
    jawaban_baru="Sertifikat elektronik dapat diunduh melalui menu 'Sertifikat Elektronik' di portal setelah proses penerbitan selesai. Klik 'Unduh' dan simpan file berformat PDF atau QR.",
    kategori_baru="Peralihan Hak Elektronik",
    sumber_baru="FAQ PPAT ATR/BPN — Peralihan Hak Elektronik"
)

# Langsung uji
hasil_tes = cari_jawaban("cara unduh sertifikat elektronik")
print(f"\nJawaban : {hasil_tes['jawaban']}")
print(f"Sumber  : {hasil_tes.get('sumber', '-')}")

"""## Chatbot Interaktif (Widget)"""

# ============================================================
# Cell 9 — UI Chatbot interaktif dengan ipywidgets
# ============================================================

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

input_pertanyaan = widgets.Text(
    value='',
    placeholder='Tulis pertanyaan seputar portal PPAT ATR/BPN...',
    description='Tanya:',
    layout=widgets.Layout(width='70%')
)

tombol_kirim = widgets.Button(
    description='Kirim',
    button_style='primary',
    tooltip='Klik untuk mendapatkan jawaban',
    icon='paper-plane'
)

output_chat = widgets.Output()

def proses_tanya(pertanyaan):
    with output_chat:
        clear_output()

        display(HTML(f'''
        <div style="background:#D6EAF8;padding:10px;border-radius:10px;
                    margin-bottom:10px;max-width:80%;float:right;clear:both;">
            <b>Anda:</b> {pertanyaan}
        </div>
        <div style="clear:both;"></div>
        '''))

        hasil = cari_jawaban(pertanyaan)

        if hasil["status"] == "Berhasil":
            display(HTML(f'''
            <div style="background:#EAF4FB;padding:12px;border-radius:10px;
                        margin-bottom:10px;max-width:80%;float:left;clear:both;
                        border-left:4px solid #2980B9;">
                <b>🤖 BPN-Bot:</b><br><br>
                {hasil["jawaban"]}<br><br>
                <small style="color:#555;">
                    <i>📂 Kategori: {hasil["kategori"]} &nbsp;|&nbsp; 🎯 Relevansi: {hasil["similarity"]}</i><br>
                    📌 Sumber: {hasil.get("sumber", "-")}
                </small>
            </div>
            <div style="clear:both;"></div>
            '''))
        else:
            opsi = "".join([
                f"<li style='margin-bottom:5px;color:#1A5276;'><b>\"{rec}\"</b></li>"
                for rec in hasil["rekomendasi"]
            ])
            display(HTML(f'''
            <div style="background:#FDFEFE;padding:12px;border-radius:10px;
                        margin-bottom:10px;max-width:80%;float:left;clear:both;
                        border-left:4px solid #E74C3C;">
                <b>🤖 BPN-Bot:</b><br><br>
                {hasil["jawaban"]}<br><br>
                <b>Mungkin Anda ingin menanyakan:</b>
                <ul style="margin-top:5px;padding-left:20px;">{opsi}</ul>
                <small style="color:#777;"><i>💡 Salin salah satu pertanyaan di atas ke kolom input.</i></small>
            </div>
            <div style="clear:both;"></div>
            '''))

def tangani_kirim(sender):
    pertanyaan = input_pertanyaan.value.strip()
    if not pertanyaan:
        return
    proses_tanya(pertanyaan)
    input_pertanyaan.value = ''

tombol_kirim.on_click(tangani_kirim)
input_pertanyaan.on_submit(tangani_kirim)

ui = widgets.VBox([
    widgets.HTML("""
        <div style="background:#2980B9;color:white;padding:14px;border-radius:8px;margin-bottom:12px;">
            <h3 style="margin:0;">🏛️ BPN-Bot — Asisten FAQ Portal PPAT ATR/BPN</h3>
            <small>Tanyakan seputar akun, akta, peralihan hak, atau kendala teknis portal.</small>
        </div>
    """),
    widgets.HBox([input_pertanyaan, tombol_kirim]),
    output_chat
])

display(ui)
