// Dataset FAQ PPAT ATR/BPN — dummy data (frontend only)

export const FAQ_DATA = [
  // ── 1. Akun, Kredensial & Autentikasi ───────────────────────
  {
    id: 1,
    pertanyaan: "Mengapa akun Mitra PPAT tidak bisa login ke Portal SSO?",
    jawaban:
      "Akun Mitra PPAT tidak bisa login ke Portal SSO umumnya disebabkan oleh: (1) Masa berlaku SK Pengangkatan/Perpanjangan sudah habis; (2) Data PPAT belum diperbarui di sistem Ditjen Penetapan Hak dan Pendaftaran Tanah; (3) Password salah atau akun terkunci. Pastikan SK masih aktif dan data sudah diperbarui oleh Kantor Pertanahan setempat.",
    kategori: "Akun, Kredensial & Autentikasi",
  },
  {
    id: 2,
    pertanyaan: "Apa penyebab akun PPAT terblokir di Portal SSO?",
    jawaban:
      "Akun PPAT dapat terblokir jika terjadi percobaan login yang gagal berulang kali (lebih dari 5 kali), atau jika sistem mendeteksi aktivitas yang mencurigakan. Tunggu 30 menit lalu coba kembali, atau ajukan pembukaan blokir melalui Helpdesk ATR/BPN.",
    kategori: "Akun, Kredensial & Autentikasi",
  },
  {
    id: 3,
    pertanyaan: "Bagaimana cara reset password akun Portal SSO PPAT?",
    jawaban:
      "Reset password dapat dilakukan di halaman login Portal SSO dengan mengklik tombol 'Lupa Password'. Masukkan alamat email terdaftar, lalu ikuti tautan yang dikirimkan ke email tersebut. Tautan reset berlaku selama 24 jam.",
    kategori: "Akun, Kredensial & Autentikasi",
  },
  {
    id: 4,
    pertanyaan: "Bagaimana cara mendaftarkan akun PPAT baru di portal mitra?",
    jawaban:
      "Pendaftaran akun PPAT baru dilakukan melalui Kantor Pertanahan setempat. Bawa SK Pengangkatan asli beserta dokumen pendukung. Petugas akan mendaftarkan akun ke sistem SSO dan mengirimkan kredensial awal ke email resmi PPAT.",
    kategori: "Akun, Kredensial & Autentikasi",
  },
  {
    id: 5,
    pertanyaan: "Kenapa kode OTP tidak masuk ke nomor HP saat login?",
    jawaban:
      "Kode OTP tidak masuk dapat disebabkan: nomor HP tidak terdaftar di sistem, gangguan jaringan provider, atau delay pengiriman SMS. Klik 'Kirim Ulang OTP' setelah 60 detik. Jika masalah berlanjut, hubungi Helpdesk untuk memverifikasi nomor HP terdaftar.",
    kategori: "Akun, Kredensial & Autentikasi",
  },

  // ── 2. Pembuatan Akta & Validasi ────────────────────────────
  {
    id: 6,
    pertanyaan: "Mengapa muncul pesan error saat membuat akta jual beli di portal?",
    jawaban:
      "Pesan error saat membuat akta jual beli umumnya terjadi karena: (1) Data bidang tanah belum lengkap atau NIK pihak tidak valid di database Dukcapil; (2) Sesi login sudah habis (timeout); (3) Format input tidak sesuai. Lakukan logout lalu login kembali, periksa kelengkapan data, dan pastikan NIK sesuai KTP aktif.",
    kategori: "Pembuatan Akta & Validasi",
  },
  {
    id: 7,
    pertanyaan: "Mengapa nomor sertifikat tidak ditemukan saat validasi di sistem?",
    jawaban:
      "Nomor sertifikat tidak ditemukan di sistem dapat berarti: (1) Data belum ter-digitasi; (2) Sertifikat diterbitkan oleh kantor pertanahan lain; (3) Terdapat kesalahan penulisan nomor. Konfirmasi kebenaran nomor dan wilayah ke Kantor Pertanahan penerbit sertifikat.",
    kategori: "Pembuatan Akta & Validasi",
  },
  {
    id: 8,
    pertanyaan: "Bagaimana format penulisan nomor hak yang benar di portal ATR/BPN?",
    jawaban:
      "Format nomor hak yang benar mengikuti pola: [Kode Kabupaten/Kota].[Kode Kecamatan].[Jenis Hak].[Nomor Urut], contoh: 3273.010.SHM.00123. Pastikan tidak ada spasi, titik tambahan, atau karakter khusus. Ikuti panduan format yang tersedia di menu Bantuan portal.",
    kategori: "Pembuatan Akta & Validasi",
  },
  {
    id: 9,
    pertanyaan: "Bagaimana cara mencetak draft akta dari portal mitra PPAT?",
    jawaban:
      "Untuk mencetak draft akta, buka menu 'Daftar Akta', pilih akta yang dimaksud, lalu klik tombol 'Unduh Draft PDF'. Pastikan browser mengizinkan pop-up dari domain portal. Gunakan browser Chrome atau Firefox versi terbaru untuk hasil optimal.",
    kategori: "Pembuatan Akta & Validasi",
  },
  {
    id: 10,
    pertanyaan: "Apa yang harus dilakukan jika data bidang tanah tidak muncul di portal?",
    jawaban:
      "Jika data bidang tanah tidak muncul, kemungkinan data bidang belum terpetakan ke wilayah kerja PPAT, atau terdapat kesalahan kode wilayah. Hubungi petugas Kantor Pertanahan untuk memastikan bidang tanah telah terdaftar dan terpetakan dengan benar.",
    kategori: "Pembuatan Akta & Validasi",
  },

  // ── 3. Peralihan Hak Elektronik & Pembayaran ────────────────
  {
    id: 11,
    pertanyaan: "Bagaimana cara mengajukan permohonan peralihan hak secara elektronik?",
    jawaban:
      "Pengajuan peralihan hak elektronik dilakukan melalui: (1) Login ke portal mitra PPAT; (2) Pilih menu 'Layanan Elektronik' → 'Peralihan Hak'; (3) Isi formulir permohonan dan unggah dokumen persyaratan; (4) Bayar kode billing yang dihasilkan sistem; (5) Pantau status melalui menu Tracking Permohonan.",
    kategori: "Peralihan Hak Elektronik & Pembayaran",
  },
  {
    id: 12,
    pertanyaan: "Apa saja dokumen yang dibutuhkan untuk peralihan hak elektronik?",
    jawaban:
      "Dokumen persyaratan peralihan hak elektronik meliputi: sertifikat asli, akta PPAT terkait, KTP seluruh pihak, bukti pembayaran BPHTB dan PPh Final, surat pernyataan sesuai jenis peralihan, serta dokumen pendukung lain sesuai ketentuan Kantor Pertanahan setempat.",
    kategori: "Peralihan Hak Elektronik & Pembayaran",
  },
  {
    id: 13,
    pertanyaan: "Berapa lama proses peralihan hak elektronik di BPN?",
    jawaban:
      "Proses peralihan hak elektronik umumnya diselesaikan dalam 5–7 hari kerja setelah berkas dinyatakan lengkap dan valid oleh petugas Kantor Pertanahan. Waktu dapat berbeda tergantung antrean dan kebijakan masing-masing Kantor Pertanahan.",
    kategori: "Peralihan Hak Elektronik & Pembayaran",
  },
  {
    id: 14,
    pertanyaan: "Mengapa kode billing SPS peralihan hak tidak muncul di portal?",
    jawaban:
      "Kode billing SPS tidak muncul biasanya karena: (1) Data formulir permohonan belum lengkap atau masih berstatus draft; (2) Sistem SPS sedang dalam pemeliharaan. Pastikan semua field wajib terisi, simpan permohonan, lalu muat ulang halaman. Jika masalah berlanjut, hubungi Helpdesk.",
    kategori: "Peralihan Hak Elektronik & Pembayaran",
  },
  {
    id: 15,
    pertanyaan: "Mengapa surat pengantar berkas peralihan hak tidak bisa dicetak?",
    jawaban:
      "Surat pengantar berkas yang tidak bisa dicetak dapat disebabkan status permohonan belum diverifikasi oleh petugas, atau koneksi internet tidak stabil saat proses generate dokumen. Periksa status permohonan di menu Tracking, lalu coba cetak ulang setelah status berubah menjadi 'Siap Cetak'.",
    kategori: "Peralihan Hak Elektronik & Pembayaran",
  },
  {
    id: 16,
    pertanyaan: "Bagaimana cara mengecek status permohonan peralihan hak elektronik?",
    jawaban:
      "Status permohonan peralihan hak dapat dipantau melalui menu 'Tracking Permohonan' di portal dengan memasukkan nomor berkas yang diperoleh saat pendaftaran. Notifikasi perubahan status juga dikirimkan melalui email terdaftar.",
    kategori: "Peralihan Hak Elektronik & Pembayaran",
  },

  // ── 4. Pelaporan Kendala Teknis ─────────────────────────────
  {
    id: 17,
    pertanyaan: "Ke mana PPAT harus melaporkan kendala teknis portal mitra?",
    jawaban:
      "Kendala teknis portal PPAT dapat dilaporkan melalui: (1) Fitur Tiket Pengaduan ANDALAS di portal; (2) Email helpdesk@atrbpn.go.id; (3) Call Center Kementerian ATR/BPN; (4) Media sosial resmi @kementerian_atrbpn. Sertakan tangkapan layar dan deskripsi langkah yang sudah dilakukan saat melapor.",
    kategori: "Pelaporan Kendala Teknis",
  },
  {
    id: 18,
    pertanyaan: "Bagaimana cara mengajukan tiket pengaduan melalui ANDALAS?",
    jawaban:
      "Tiket pengaduan ANDALAS diajukan melalui menu 'Tiket Pengaduan' di portal. Pilih kategori masalah yang sesuai, deskripsikan kendala secara detail, lampirkan tangkapan layar jika ada, lalu klik Kirim. Nomor tiket akan dikirimkan ke email untuk keperluan pemantauan.",
    kategori: "Pelaporan Kendala Teknis",
  },
  {
    id: 19,
    pertanyaan: "Bagaimana cara menghubungi helpdesk ATR/BPN untuk kendala portal?",
    jawaban:
      "Helpdesk ATR/BPN dapat dihubungi melalui portal Sentuh Tanahku, email helpdesk@atrbpn.go.id, atau melalui halaman Pusat Kontak & Bantuan di bantuan.atrbpn.go.id. Jam layanan Helpdesk adalah Senin–Jumat pukul 08.00–16.00 WIB.",
    kategori: "Pelaporan Kendala Teknis",
  },
  {
    id: 20,
    pertanyaan: "Apakah tersedia panduan pengguna portal mitra PPAT?",
    jawaban:
      "Panduan pengguna portal Mitra PPAT tersedia di menu 'Bantuan' → 'Unduh Panduan' di portal. Panduan juga dapat diakses melalui halaman bantuan.atrbpn.go.id pada bagian Tanya Jawab (FAQ) dan artikel panduan teknis.",
    kategori: "Pelaporan Kendala Teknis",
  },

  // ── 5. Hak Tanggungan Elektronik ────────────────────────────
  {
    id: 21,
    pertanyaan: "Apa itu Hak Tanggungan Elektronik di portal ATR/BPN?",
    jawaban:
      "Hak Tanggungan Elektronik (HT-el) adalah layanan pendaftaran hak tanggungan secara daring yang diintegrasikan dalam Portal Mitra ATR/BPN. Layanan ini memungkinkan PPAT mendaftarkan Akta Pembebanan Hak Tanggungan (APHT) dan Surat Kuasa Membebankan Hak Tanggungan (SKMHT) tanpa harus datang ke kantor pertanahan.",
    kategori: "Hak Tanggungan Elektronik",
  },
  {
    id: 22,
    pertanyaan: "Bagaimana cara mendaftarkan Hak Tanggungan secara elektronik?",
    jawaban:
      "Pendaftaran Hak Tanggungan Elektronik dilakukan melalui: (1) Login portal mitra PPAT; (2) Pilih menu 'Hak Tanggungan Elektronik'; (3) Isi data debitur, kreditur, dan objek jaminan; (4) Unggah APHT dan dokumen pendukung; (5) Bayar PNBP melalui kode billing yang digenerate sistem; (6) Pantau status pendaftaran.",
    kategori: "Hak Tanggungan Elektronik",
  },
  {
    id: 23,
    pertanyaan: "Mengapa APHT tidak bisa diajukan secara elektronik?",
    jawaban:
      "APHT tidak bisa diajukan secara elektronik biasanya karena: (1) Data sertifikat belum ter-mapping di sistem HT-el; (2) PPAT belum terdaftar sebagai pengguna layanan HT-el; (3) Terdapat ketidaksesuaian data kreditur dengan sistem OJK. Hubungi Kantor Pertanahan untuk aktivasi akses HT-el.",
    kategori: "Hak Tanggungan Elektronik",
  },

  // ── 6. KJKSB ────────────────────────────────────────────────
  {
    id: 24,
    pertanyaan: "Apa itu KJKSB dalam layanan pertanahan ATR/BPN?",
    jawaban:
      "KJKSB (Kegiatan Jual-beli, Kredit, Sewa-menyewa, dan Berbagi) adalah layanan pencatatan transaksi pertanahan berbasis digital di portal ATR/BPN yang bertujuan meningkatkan transparansi dan pengawasan transaksi properti di Indonesia.",
    kategori: "KJKSB",
  },
  {
    id: 25,
    pertanyaan: "Bagaimana cara mengakses layanan KJKSB melalui portal?",
    jawaban:
      "Layanan KJKSB dapat diakses melalui menu 'KJKSB' di portal mitra PPAT setelah login menggunakan akun SSO. Pilih jenis transaksi yang sesuai, isi data pihak dan objek tanah, lalu ikuti alur pengisian yang tersedia.",
    kategori: "KJKSB",
  },
  {
    id: 26,
    pertanyaan: "Dokumen apa saja yang diperlukan untuk permohonan KJKSB?",
    jawaban:
      "Dokumen yang diperlukan untuk permohonan KJKSB meliputi: identitas para pihak (KTP/Paspor), dokumen kepemilikan tanah (sertifikat), akta/perjanjian terkait transaksi, bukti pembayaran pajak terkait, serta dokumen pendukung sesuai jenis kegiatan.",
    kategori: "KJKSB",
  },

  // ── 7. KKPR Non Berusaha & Stranas ──────────────────────────
  {
    id: 27,
    pertanyaan: "Apa itu KKPR Non Berusaha dalam layanan ATR/BPN?",
    jawaban:
      "KKPR Non Berusaha (Kesesuaian Kegiatan Pemanfaatan Ruang untuk Non Usaha) adalah persetujuan pemanfaatan ruang yang diperuntukkan bagi kegiatan yang tidak bersifat komersial, seperti pembangunan rumah tinggal atau fasilitas sosial oleh perorangan.",
    kategori: "KKPR Non Berusaha & Stranas",
  },
  {
    id: 28,
    pertanyaan: "Bagaimana cara mengajukan permohonan KKPR Non Berusaha?",
    jawaban:
      "Permohonan KKPR Non Berusaha diajukan secara daring melalui portal OSS (Online Single Submission) di oss.go.id atau melalui dinas terkait. PPAT dapat membantu klien dalam mempersiapkan dokumen persyaratan teknis seperti peta bidang dan data kepemilikan tanah.",
    kategori: "KKPR Non Berusaha & Stranas",
  },
  {
    id: 29,
    pertanyaan: "Apa itu Stranas dalam konteks layanan pertanahan?",
    jawaban:
      "Stranas (Strategi Nasional) dalam konteks pertanahan merujuk pada program prioritas nasional bidang pertanahan yang meliputi redistribusi tanah, legalisasi aset, dan penyelesaian konflik agraria sebagai bagian dari Reforma Agraria yang dikoordinasikan Kementerian ATR/BPN.",
    kategori: "KKPR Non Berusaha & Stranas",
  },
];

export const KATEGORI_LIST = [
  { id: "semua", label: "Semua Topik", icon: "🏛️" },
  { id: "Akun, Kredensial & Autentikasi", label: "Akun, Kredensial & Autentikasi", icon: "🔐" },
  { id: "Pembuatan Akta & Validasi", label: "Pembuatan Akta & Validasi", icon: "📄" },
  { id: "Peralihan Hak Elektronik & Pembayaran", label: "Peralihan Hak Elektronik & Pembayaran", icon: "🔄" },
  { id: "Pelaporan Kendala Teknis", label: "Pelaporan Kendala Teknis", icon: "🛠️" },
  { id: "Hak Tanggungan Elektronik", label: "Hak Tanggungan Elektronik", icon: "🏦" },
  { id: "KJKSB", label: "KJKSB", icon: "🤝" },
  { id: "KKPR Non Berusaha & Stranas", label: "KKPR Non Berusaha & Stranas", icon: "🗺️" },
];
