// Konten artikel/penjelasan per topik — ditampilkan di halaman utama

export const TOPIK_LIST = [
  { id: "beranda", icon: "🏠", label: "Beranda" },
  { id: "akun",    icon: "🔐", label: "Akun, Kredensial & Autentikasi" },
  { id: "akta",    icon: "📄", label: "Pembuatan Akta & Validasi" },
  { id: "peralihan", icon: "🔄", label: "Peralihan Hak Elektronik" },
  { id: "kendala", icon: "🛠️", label: "Pelaporan Kendala Teknis" },
  { id: "ht",      icon: "🏦", label: "Hak Tanggungan Elektronik" },
  { id: "kjksb",   icon: "🤝", label: "KJKSB" },
  { id: "kkpr",    icon: "🗺️", label: "KKPR Non Berusaha & Stranas" },
];

export const KONTEN_TOPIK = {
  beranda: {
    icon: "🏛️",
    judul: "FAQ PPAT — Portal Mitra Kerja ATR/BPN",
    subjudul: "Halaman ini memuat panduan teknis yang paling sering dibutuhkan oleh Pejabat Pembuat Akta Tanah (PPAT) dalam penggunaan Portal Mitra Kerja Kementerian ATR/BPN.",
    seksi: [
      {
        judul: "Apa itu Portal Mitra PPAT?",
        isi: "Portal Mitra PPAT adalah aplikasi berbasis web yang disediakan oleh Kementerian ATR/BPN untuk mendukung tugas PPAT secara digital. Melalui portal ini, PPAT dapat membuat dan mengelola akta, mengajukan peralihan hak, mendaftarkan Hak Tanggungan, serta melaporkan kegiatan pertanahan secara elektronik tanpa harus datang langsung ke Kantor Pertanahan.",
      },
      {
        judul: "Siapa yang bisa mengakses portal ini?",
        isi: "Portal ini diperuntukkan bagi PPAT yang telah diangkat secara resmi oleh Menteri ATR/BPN dan memiliki SK Pengangkatan yang masih berlaku. Staf kantor PPAT juga dapat diberikan akses terbatas atas izin PPAT yang bersangkutan.",
      },
      {
        judul: "Topik yang tersedia di halaman ini",
        isi: "Pilih salah satu topik di menu sebelah kiri untuk membaca penjelasan lengkap. Tersedia panduan tentang akun SSO, pembuatan akta, peralihan hak elektronik, Hak Tanggungan Elektronik (HT-el), KJKSB, KKPR, dan cara melaporkan kendala teknis.",
      },
      {
        judul: "Butuh jawaban cepat?",
        isi: "Gunakan BPN-Bot di pojok kanan bawah untuk mengajukan pertanyaan secara langsung. BPN-Bot akan memberikan jawaban berdasarkan database FAQ Portal Mitra PPAT ATR/BPN.",
      },
    ],
  },

  akun: {
    icon: "🔐",
    judul: "Akun, Kredensial & Autentikasi",
    subjudul: "Panduan lengkap mengelola akun Portal SSO PPAT — mulai dari pendaftaran, login, OTP, hingga penanganan akun terblokir.",
    seksi: [
      {
        judul: "Cara mendapatkan akun Portal SSO",
        isi: "Akun Portal SSO PPAT dibuat oleh petugas Kantor Pertanahan setempat berdasarkan data SK Pengangkatan PPAT yang masih aktif. PPAT cukup datang ke Kantor Pertanahan dengan membawa SK Pengangkatan asli dan dokumen identitas. Petugas akan mendaftarkan akun dan mengirimkan kredensial awal (email + password sementara) ke email resmi PPAT.",
      },
      {
        judul: "Mengapa akun tidak bisa login?",
        isi: "Ada beberapa kemungkinan penyebab akun Mitra PPAT tidak bisa login ke Portal SSO:\n• Masa berlaku SK Pengangkatan atau SK Perpanjangan sudah habis.\n• Data PPAT belum diperbarui di sistem Ditjen Penetapan Hak dan Pendaftaran Tanah.\n• Password salah atau akun dalam status terkunci.\n• Akun terblokir akibat terlalu banyak percobaan login yang gagal.\n\nSolusi: Pastikan SK masih aktif, verifikasi data ke Kantor Pertanahan, dan gunakan fitur 'Lupa Password' jika lupa kata sandi.",
      },
      {
        judul: "Cara reset password",
        isi: "Reset password dapat dilakukan mandiri melalui halaman login Portal SSO:\n1. Klik tombol 'Lupa Password' di halaman login.\n2. Masukkan alamat email yang terdaftar.\n3. Buka email masuk dan klik tautan reset yang dikirimkan.\n4. Buat password baru yang kuat (minimal 8 karakter, kombinasi huruf dan angka).\n\nPenting: Tautan reset password hanya berlaku selama 24 jam. Jika sudah kedaluwarsa, ulangi proses dari awal.",
      },
      {
        judul: "Kode OTP tidak masuk",
        isi: "Kode OTP dikirimkan ke nomor HP yang terdaftar di akun. Jika tidak masuk:\n• Pastikan nomor HP yang terdaftar masih aktif dan memiliki sinyal.\n• Tunggu hingga 60 detik sebelum meminta pengiriman ulang.\n• Klik 'Kirim Ulang OTP' untuk meminta kode baru.\n• Jika nomor HP sudah berganti, hubungi Kantor Pertanahan untuk memperbarui data.",
      },
      {
        judul: "Akun terblokir",
        isi: "Akun akan otomatis terblokir setelah 5 kali percobaan login yang gagal secara berturut-turut sebagai langkah keamanan sistem. Langkah penanganan:\n• Tunggu 30 menit — sistem akan membuka blokir secara otomatis.\n• Jika setelah 30 menit masih terblokir, ajukan permintaan buka blokir melalui Helpdesk ATR/BPN.\n• Sertakan nama lengkap, nomor SK, dan alamat email terdaftar saat menghubungi Helpdesk.",
      },
    ],
  },

  akta: {
    icon: "📄",
    judul: "Pembuatan Akta & Validasi Data",
    subjudul: "Panduan teknis membuat akta melalui portal, melakukan validasi data pihak dan sertifikat, serta mengatasi error yang umum terjadi.",
    seksi: [
      {
        judul: "Alur pembuatan akta di portal",
        isi: "Pembuatan akta melalui Portal Mitra PPAT mengikuti alur berikut:\n1. Login ke portal menggunakan akun SSO.\n2. Pilih menu 'Pembuatan Akta' dan tentukan jenis akta.\n3. Masukkan data bidang tanah — nomor sertifikat akan divalidasi otomatis ke database BPN.\n4. Masukkan data pihak (penjual/pembeli/debitur) — NIK divalidasi ke database Dukcapil.\n5. Periksa dan konfirmasi seluruh data.\n6. Unduh draft akta dalam format PDF untuk ditandatangani.",
      },
      {
        judul: "Format nomor hak yang benar",
        isi: "Penulisan nomor hak di portal harus mengikuti format standar:\n[Kode Kabupaten/Kota].[Kode Kecamatan].[Jenis Hak].[Nomor Urut]\n\nContoh: 3273.010.SHM.00123\n• 3273 = Kode Kota Bandung\n• 010  = Kode Kecamatan\n• SHM  = Jenis hak (Sertifikat Hak Milik)\n• 00123 = Nomor urut\n\nPastikan tidak ada spasi, titik ekstra, atau karakter khusus lainnya.",
      },
      {
        judul: "Nomor sertifikat tidak ditemukan",
        isi: "Jika nomor sertifikat tidak ditemukan saat validasi, kemungkinan penyebabnya:\n• Data sertifikat belum ter-digitasi ke sistem BPN.\n• Sertifikat diterbitkan oleh kantor pertanahan yang berbeda.\n• Terdapat kesalahan penulisan nomor atau kode wilayah.\n\nSolusi: Konfirmasikan kebenaran nomor sertifikat dan kode wilayah ke Kantor Pertanahan penerbit sertifikat tersebut.",
      },
      {
        judul: "Error validasi NIK",
        isi: "Error validasi NIK terjadi ketika NIK yang dimasukkan tidak ditemukan atau tidak sesuai di database Dukcapil. Penyebab umum:\n• NIK diinput dengan tidak lengkap atau ada kesalahan angka.\n• KTP yang digunakan sudah tidak aktif atau masa berlaku habis.\n• Data kependudukan belum diperbarui di Dukcapil setempat.\n\nSolusi: Pastikan menggunakan NIK dari KTP aktif, periksa ulang angka satu per satu, dan minta pihak memperbarui data di Disdukcapil jika diperlukan.",
      },
      {
        judul: "Mencetak draft akta",
        isi: "Draft akta dapat dicetak melalui menu 'Daftar Akta':\n1. Buka menu Daftar Akta.\n2. Temukan akta yang dimaksud berdasarkan nomor atau tanggal.\n3. Klik tombol 'Unduh Draft PDF'.\n\nJika tombol unduh tidak berfungsi:\n• Pastikan browser mengizinkan pop-up dari domain portal.\n• Gunakan Chrome atau Firefox versi terbaru.\n• Nonaktifkan sementara ekstensi pemblokir pop-up.",
      },
    ],
  },

  peralihan: {
    icon: "🔄",
    judul: "Peralihan Hak Elektronik & Pembayaran",
    subjudul: "Panduan mengajukan permohonan peralihan hak tanah secara elektronik, melakukan pembayaran melalui kode billing SPS, dan memantau status permohonan.",
    seksi: [
      {
        judul: "Apa itu peralihan hak elektronik?",
        isi: "Peralihan hak elektronik adalah layanan yang memungkinkan PPAT mengajukan permohonan balik nama, pewarisan, hibah, dan jenis peralihan hak lainnya secara daring melalui Portal Mitra tanpa harus menyerahkan berkas fisik langsung ke loket Kantor Pertanahan.",
      },
      {
        judul: "Langkah-langkah pengajuan",
        isi: "Cara mengajukan peralihan hak secara elektronik:\n1. Login ke portal mitra PPAT.\n2. Pilih menu Layanan Elektronik → Peralihan Hak.\n3. Pilih jenis peralihan yang sesuai.\n4. Isi formulir dan unggah dokumen persyaratan.\n5. Sistem akan menerbitkan kode billing SPS untuk pembayaran.\n6. Lakukan pembayaran sesuai kode billing.\n7. Status permohonan dapat dipantau di menu Tracking Permohonan.",
      },
      {
        judul: "Dokumen persyaratan",
        isi: "Dokumen yang wajib disiapkan untuk peralihan hak elektronik:\n• Sertifikat asli bidang tanah yang dialihkan.\n• Akta PPAT terkait (jual beli, hibah, waris, dsb).\n• KTP seluruh pihak yang terlibat.\n• Bukti pembayaran BPHTB (Bea Perolehan Hak atas Tanah dan Bangunan).\n• Bukti pembayaran PPh Final (untuk transaksi jual beli).\n• Surat pernyataan sesuai jenis peralihan.\n• Dokumen tambahan sesuai ketentuan Kantor Pertanahan setempat.",
      },
      {
        judul: "Kode billing SPS tidak muncul",
        isi: "Kode billing SPS akan digenerate otomatis setelah semua data formulir terisi lengkap dan valid. Jika tidak muncul:\n• Periksa kembali apakah semua field wajib sudah diisi.\n• Pastikan status permohonan bukan lagi 'Draft'.\n• Muat ulang halaman dan cek kembali.\n• Jika masalah berlanjut, kemungkinan sistem SPS sedang dalam pemeliharaan — hubungi Helpdesk.",
      },
      {
        judul: "Lama proses dan tracking",
        isi: "Proses peralihan hak elektronik umumnya diselesaikan dalam 5–7 hari kerja setelah berkas dinyatakan lengkap dan valid oleh petugas Kantor Pertanahan. Waktu dapat bervariasi tergantung antrean masing-masing kantor.\n\nUntuk memantau status, gunakan menu Tracking Permohonan dengan memasukkan nomor berkas. Notifikasi perubahan status juga dikirim otomatis ke email terdaftar.",
      },
    ],
  },

  kendala: {
    icon: "🛠️",
    judul: "Pelaporan Kendala Teknis Portal",
    subjudul: "Cara melaporkan masalah teknis yang ditemui saat menggunakan Portal Mitra PPAT, termasuk saluran pengaduan dan informasi layanan Helpdesk.",
    seksi: [
      {
        judul: "Saluran pelaporan kendala",
        isi: "Kendala teknis portal dapat dilaporkan melalui beberapa saluran:\n• Tiket Pengaduan ANDALAS: Melalui menu 'Tiket Pengaduan' di dalam portal.\n• Email: helpdesk@atrbpn.go.id\n• Media sosial resmi: @kementerian_atrbpn\n• Kantor Pertanahan setempat untuk kendala yang memerlukan tindakan langsung.\n\nSaat melapor, sertakan tangkapan layar error, deskripsi langkah yang sudah dilakukan, dan nomor akun PPAT.",
      },
      {
        judul: "Cara mengajukan tiket ANDALAS",
        isi: "ANDALAS adalah sistem pengaduan resmi layanan pertanahan digital ATR/BPN. Langkah pengajuan:\n1. Login ke portal, buka menu Tiket Pengaduan.\n2. Klik 'Buat Tiket Baru'.\n3. Pilih kategori masalah yang sesuai.\n4. Deskripsikan kendala secara detail dan spesifik.\n5. Lampirkan tangkapan layar jika ada.\n6. Klik Kirim.\n\nNomor tiket akan dikirimkan ke email untuk keperluan pemantauan tindak lanjut.",
      },
      {
        judul: "Jam layanan Helpdesk",
        isi: "Helpdesk ATR/BPN melayani pertanyaan dan pengaduan pada:\n• Hari: Senin–Jumat\n• Jam: 08.00–16.00 WIB\n• Email: helpdesk@atrbpn.go.id\n• Portal bantuan: bantuan.atrbpn.go.id\n\nDi luar jam kerja, laporan tetap dapat disampaikan melalui email atau ANDALAS dan akan ditindaklanjuti pada hari kerja berikutnya.",
      },
      {
        judul: "Panduan pengguna portal",
        isi: "Panduan lengkap penggunaan Portal Mitra PPAT tersedia dalam format PDF dan dapat diunduh melalui:\n• Menu Bantuan → Unduh Panduan di dalam portal.\n• Halaman bantuan.atrbpn.go.id pada bagian Tanya Jawab (FAQ).\n• Artikel panduan teknis yang diperbarui secara berkala oleh tim ATR/BPN.",
      },
    ],
  },

  ht: {
    icon: "🏦",
    judul: "Hak Tanggungan Elektronik (HT-el)",
    subjudul: "Layanan pendaftaran Hak Tanggungan secara daring yang terintegrasi di Portal Mitra ATR/BPN — tanpa perlu datang ke Kantor Pertanahan.",
    seksi: [
      {
        judul: "Apa itu HT-el?",
        isi: "Hak Tanggungan Elektronik (HT-el) adalah sistem pendaftaran Hak Tanggungan berbasis digital yang memungkinkan PPAT mendaftarkan Akta Pembebanan Hak Tanggungan (APHT) dan Surat Kuasa Membebankan Hak Tanggungan (SKMHT) secara daring.\n\nLayanan ini diatur dalam Peraturan Menteri ATR/BPN No. 5 Tahun 2020 dan bertujuan mempercepat proses pendaftaran serta mengurangi interaksi fisik di loket.",
      },
      {
        judul: "Cara mendaftarkan HT-el",
        isi: "Langkah pendaftaran Hak Tanggungan Elektronik:\n1. Login ke Portal Mitra PPAT.\n2. Pilih menu Hak Tanggungan Elektronik.\n3. Isi data debitur (pihak peminjam), kreditur (bank/lembaga), dan objek jaminan.\n4. Unggah APHT yang telah ditandatangani dan dokumen pendukung lainnya.\n5. Sistem akan menghitung dan menerbitkan kode billing PNBP.\n6. Lakukan pembayaran PNBP sesuai kode billing.\n7. Pantau status pendaftaran secara real-time di portal.",
      },
      {
        judul: "Biaya PNBP HT-el",
        isi: "Biaya Penerimaan Negara Bukan Pajak (PNBP) untuk pendaftaran HT-el dihitung secara otomatis oleh sistem berdasarkan nilai tanggungan yang dicantumkan dalam APHT, sesuai dengan tarif yang diatur dalam Peraturan Pemerintah tentang PNBP Kementerian ATR/BPN.\n\nUntuk simulasi biaya, gunakan kalkulator PNBP yang tersedia di halaman formulir HT-el sebelum melakukan pengajuan resmi.",
      },
      {
        judul: "Aktivasi akses HT-el",
        isi: "Tidak semua akun PPAT otomatis memiliki akses ke layanan HT-el. Jika menu HT-el tidak muncul atau APHT tidak bisa diajukan:\n• Pastikan data sertifikat objek jaminan sudah ter-mapping di sistem HT-el.\n• Pastikan akun PPAT sudah diaktifkan sebagai pengguna layanan HT-el.\n• Periksa apakah data kreditur sudah sesuai dengan data lembaga di sistem OJK.\n\nUntuk aktivasi, hubungi Kantor Pertanahan setempat.",
      },
      {
        judul: "Kemerdekaan Indonesia",
        isi: "indonesia merdeka pada 17 agustus 1945:\n• Presiden IR.Soekarno.\n• wakilnya bernama Muhammad Hatta \n•",
      },
    ],
  },

  kjksb: {
    icon: "🤝",
    judul: "KJKSB — Kegiatan Jual-beli, Kredit, Sewa-menyewa & Berbagi",
    subjudul: "Layanan pencatatan transaksi pertanahan berbasis digital untuk meningkatkan transparansi dan pengawasan transaksi properti nasional.",
    seksi: [
      {
        judul: "Apa itu KJKSB?",
        isi: "KJKSB adalah singkatan dari Kegiatan Jual-beli, Kredit, Sewa-menyewa, dan Berbagi. Ini adalah kewajiban pelaporan yang harus dilakukan PPAT setiap kali membuat akta yang berkaitan dengan keempat jenis kegiatan tersebut.\n\nTujuannya adalah menciptakan sistem monitoring transaksi pertanahan yang transparan dan dapat diawasi secara nasional oleh Kementerian ATR/BPN.",
      },
      {
        judul: "Cara mengakses dan melaporkan KJKSB",
        isi: "Pelaporan KJKSB dilakukan melalui:\n1. Login ke Portal Mitra PPAT.\n2. Buka menu KJKSB.\n3. Pilih jenis kegiatan: Jual-beli, Kredit, Sewa-menyewa, atau Berbagi.\n4. Isi data pihak-pihak yang terlibat dan objek tanah.\n5. Lampirkan akta/perjanjian terkait.\n6. Submit laporan.\n\nPelaporan wajib dilakukan dalam jangka waktu yang ditentukan setelah akta dibuat.",
      },
      {
        judul: "Dokumen yang diperlukan",
        isi: "Dokumen yang dibutuhkan untuk pelaporan KJKSB:\n• KTP atau paspor seluruh pihak yang terlibat dalam transaksi.\n• Sertifikat tanah yang menjadi objek transaksi.\n• Akta atau perjanjian yang dibuat oleh PPAT.\n• Bukti pembayaran pajak terkait (BPHTB, PPh, PPN jika ada).\n• Dokumen tambahan sesuai jenis kegiatan yang dilaporkan.",
      },
      {
        judul: "Sanksi keterlambatan pelaporan",
        isi: "Pelaporan KJKSB bersifat wajib bagi PPAT. Keterlambatan atau kelalaian dalam pelaporan dapat berdampak pada:\n• Catatan kepatuhan PPAT di sistem pengawasan ATR/BPN.\n• Potensi sanksi administratif sesuai ketentuan yang berlaku.\n\nPastikan selalu melaporkan setiap transaksi tepat waktu sesuai ketentuan yang berlaku.",
      },
    ],
  },

  kkpr: {
    icon: "🗺️",
    judul: "KKPR Non Berusaha & Stranas",
    subjudul: "Informasi tentang Kesesuaian Kegiatan Pemanfaatan Ruang untuk non-usaha dan program Strategi Nasional pertanahan Reforma Agraria.",
    seksi: [
      {
        judul: "Apa itu KKPR Non Berusaha?",
        isi: "KKPR (Kesesuaian Kegiatan Pemanfaatan Ruang) Non Berusaha adalah persetujuan resmi dari pemerintah yang menyatakan bahwa suatu kegiatan non-komersial sesuai dengan tata ruang wilayah setempat.\n\nContoh kegiatan yang memerlukan KKPR Non Berusaha:\n• Pembangunan rumah tinggal oleh perorangan.\n• Pembangunan fasilitas sosial atau keagamaan.\n• Kegiatan pertanian skala kecil oleh petani.",
      },
      {
        judul: "Cara mengajukan KKPR Non Berusaha",
        isi: "Permohonan KKPR Non Berusaha diajukan secara daring melalui:\n• Portal OSS (Online Single Submission) di oss.go.id\n• Atau melalui Dinas Penanaman Modal dan PTSP setempat.\n\nPeran PPAT: Membantu klien menyiapkan dokumen teknis pertanahan seperti peta bidang tanah, surat kepemilikan, dan data koordinat lokasi yang diperlukan dalam proses pengajuan.",
      },
      {
        judul: "Apa itu Stranas?",
        isi: "Stranas (Strategi Nasional) dalam konteks pertanahan merujuk pada program prioritas nasional bidang pertanahan yang dikoordinasikan oleh Kementerian ATR/BPN sebagai bagian dari agenda Reforma Agraria.\n\nProgram Stranas mencakup:\n• Redistribusi tanah — pembagian tanah kepada masyarakat yang berhak.\n• Legalisasi aset — penerbitan sertifikat tanah bagi tanah yang belum bersertifikat.\n• Penyelesaian konflik agraria — mediasi dan penyelesaian sengketa tanah.\n• Penataan kawasan dan pengakuan tanah ulayat.",
      },
      {
        judul: "Peran PPAT dalam program Stranas",
        isi: "PPAT yang wilayah kerjanya masuk dalam lokus program Stranas dapat berkontribusi melalui:\n• Melaporkan transaksi pertanahan terkait objek redistribusi melalui menu Laporan Stranas di portal.\n• Membantu masyarakat dalam proses legalisasi aset dengan membuatkan akta yang diperlukan.\n• Berkoordinasi dengan Kantor Pertanahan setempat untuk memastikan data transaksi tercatat dalam sistem Stranas.",
      },
    ],
  },
};
