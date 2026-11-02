# Math Adventure: Fraction Kingdom

**Versi 1.2 — Siap GitHub Pages & Vercel (2 November 2026)**

**Game edukasi Matematika kelas 6 SD** — platformer pixel art 2D orisinal dengan kotak soal, combo sampai x5, 3 dunia, final boss, serta Hall of Fame.

> **Status:** Kode permainan lengkap dan dapat berjalan sebagai aplikasi web statis tanpa layanan eksternal. Build diuji berhasil. Pengujian unit/simulasi interaksi menu, lompatan mengenai kotak, pilihan jawaban, dan kembali bermain lulus. Pengujian visual lintas-perangkat di browser nyata tetap disarankan sebelum pemakaian di kelas.

## Perbaikan grafis versi 1.1

- **Perbaikan posisi tekstur saat kamera bergeser:** lantai tidak lagi digambar dengan offset kamera ganda. Tekstur sekarang mengikuti *collision hitbox* dan posisi karakter pada setiap level.
- **Tekstur tanah tanpa garis rumput berulang:** lapisan paling atas memakai rumput, sedangkan lapisan tanah bawah memakai sprite tanah terpisah.
- **Platform mengambang tidak lagi dipipihkan:** menggunakan sprite platform baru dengan tinggi tepat 20 piksel.
- **Tepi jurang rapi:** setiap segmen tanah di-*clip* pada batas fisiknya; tidak ada tile yang menggambar melewati ujung tanah.
- **Jurang lebih terbaca:** warna dinding dan permukaan air/lava lebih jelas, bukan bukit latar yang terlihat seperti tanah hilang.
- **Pohon dekoratif hanya digambar di area yang memiliki tanah**, tidak lagi melayang di atas celah jurang.
- Koreksi dilakukan untuk **ketiga level**, bukan hanya Fraction Forest.

**Penting:** Pembaruan ini mempertahankan data skor lokal lama jika dimainkan di alamat dan browser yang sama, dan tidak mengubah bank 120 soal atau aturan poin.

## Cara menjalankan

Persyaratan: **Node.js 18+**. Tidak ada library eksternal yang wajib diunduh.

```bash
npm install
npm run dev
```

Buka **http://localhost:4173** di browser. Atau untuk produksi:

```bash
npm run build
npm run preview
```

Folder hasil build: `dist/`. Alternatif: jalankan static HTTP server di root proyek. Akses langsung melalui `file://` tidak direkomendasikan karena pembatasan browser pada modul JavaScript.

## Fitur

- Kontrol **← → / A D**, **Spasi / W / ↑** untuk melompat, **Shift** untuk berlari, **P/Esc** untuk jeda; kontrol sentuh pada perangkat dengan pointer sentuh.
- Dunia 1: **Fraction Forest** — 10 kotak soal penjumlahan/pengurangan pecahan.
- Dunia 2: **Fraction Cave** — 12 kotak soal perkalian, pembagian, pecahan campuran dan desimal.
- Dunia 3: **Ratio Castle** — 15 kotak soal perbandingan senilai/berbalik nilai, dengan final boss **King Ratio** (5 jawaban benar untuk menang).
- Total **120 soal bawaan** dengan 4 pilihan unik per soal, pembahasan, dan pengacakan urutan pilihan.
- Skor: benar berturut-turut **100, 200, 300, 400, 500**, maksimal **x5**; salah mereset combo; koin **+10**.
- **3 nyawa**, musuh yang bisa diinjak, jurang, checkpoint, penyimpanan pencapaian level.
- **Hall of Fame** top 10; wajib memasukkan nama untuk menyimpan hasil, opsi skor terbaik per siswa, ekspor CSV.
- **Mode Guru**: menambahkan/menghapus soal kustom, impor JSON/CSV, ekspor bank soal, ekspor skor, serta filter tingkat kesulitan.
- Musik dan efek suara sintetis orisinal; pengaturan musik/SFX, volume, fullscreen.
- Penyimpanan offline pada `localStorage`. Pilihan database online Supabase tersedia melalui `config.js`.

## Format impor soal

JSON berupa array:

```json
[
  {
    "question": "Hasil 1/2 + 1/4 adalah ...",
    "options": ["1/4", "2/4", "3/4", "1"],
    "answer": 2,
    "category": "fraction-add",
    "difficulty": "mudah",
    "explanation": "1/2 = 2/4, lalu 2/4 + 1/4 = 3/4"
  }
]
```

`answer` menggunakan indeks **0=A, 1=B, 2=C, 3=D**. Kategori: `fraction-add`, `fraction-mul`, `mixed`, `direct`, `inverse`. Kesulitan: `mudah`, `sedang`, `sulit`.

Format CSV mengharuskan header:

```
question,option_a,option_b,option_c,option_d,answer,category,difficulty,explanation
```

Dalam CSV kolom `answer` boleh 0–3 atau A–D. Gunakan tanda kutip ganda sesuai standar CSV apabila teks mengandung koma. File impor maksimal 300 soal sekali unggah.

## GitHub Pages dan Vercel (versi siap online)

**Panduan langkah demi langkah tersedia di [`GITHUB-VERCEL.md`](GITHUB-VERCEL.md).**

- **GitHub Pages:** workflow otomatis `.github/workflows/deploy-pages.yml` menguji, membangun, dan menerbitkan game saat push ke `main`. Anda perlu membuat repository sendiri lalu mengaktifkan `Settings → Pages → GitHub Actions`.
- **Vercel:** import repository GitHub dan pilih `Framework: Other`, `Build Command: npm run build`, `Output Directory: dist` (juga dikonfigurasi di `vercel.json`).
- **Hall of Fame online:** opsional Supabase. Tanpa Supabase, leaderboard hanya lokal pada browser setiap pemain.
- **Perintah verifikasi sebelum push:** `npm test && npm run build`.

**Belum ada URL publik sampai pemilik repository menyelesaikan pengunggahan dan deployment.**

## Hall of Fame Online melalui Supabase (opsional)

Tanpa konfigurasi, papan skor hanya lokal pada browser itu. Untuk berbagi nilai di beberapa perangkat, buat project Supabase dan jalankan SQL pada `supabase-schema.sql` terlebih dahulu. Lalu edit **`public/config.js`**:

```js
window.MATH_ADVENTURE_CONFIG = {
  supabaseUrl: 'https://PROJECT.supabase.co',
  supabaseAnonKey: 'SUPABASE_PUBLISHABLE_OR_ANON_KEY'
};
```

Kemudian deploy ulang. Jangan pernah memasukkan **service_role / secret key** ke file frontend. Jika sambungan gagal, penyimpanan kembali ke perangkat lokal. Skor yang disimpan lokal saat offline **tidak otomatis tersinkron kembali**; ekspor CSV digunakan untuk arsip.

**Catatan privasi dan keamanan penting:** SQL contoh adalah mode demonstrasi dengan pembacaan dan pengiriman skor anonim. Untuk penggunaan di sekolah, gunakan nama samaran/inisial alih-alih data identitas lengkap, atau tambahkan sistem autentikasi sekolah dan kebijakan akses per kelas. Skor dikirim dari browser dan **dapat dimanipulasi**; sebelum menjadikannya kompetisi resmi, verifikasi hasil di server. Panel guru offline tidak dilindungi login—didesain untuk dipakai di perangkat guru.

## Keterangan teknis

Spesifikasi awal menyebut Phaser 3 + Vite, tetapi dependensi tidak dapat diunduh di lingkungan pembuatan. Agar benar-benar dapat dimainkan, versi ini menggunakan **HTML5 Canvas + JavaScript standar + server/build Node.js bawaan**, tanpa Phaser maupun Vite. Mekanika platformer, collision, side-scrolling, dan respons input diimplementasikan sendiri. Keuntungannya: proyek bisa di-build tanpa mengunduh paket, dapat dimainkan offline setelah di-host secara lokal, dan siap deploy statis.

Aset karakter, latar, blok, koin, musuh, dan bos adalah **pixel art orisinal** yang dibuat secara prosedural (skrip `make_assets.py`); tidak menyertakan karakter atau aset Nintendo.

## Struktur proyek

```
index.html                  UI game dan menu
styles.css                  Responsive layout, dialog, mobile controls
src/main.js                 Game loop, fisika, input, render, quiz, HUD
src/questions.js            Manajemen dan validasi bank soal
src/questions-data.js       120 soal bawaan
src/leaderboard.js          Penyimpanan lokal dan opsi Supabase
public/assets/             15 aset pixel art orisinal
public/config.js            Konfigurasi Supabase opsional
public/questions.json       120 soal (format impor)
make_assets.py              Pembuat sprite/benda pixel art
make_questions.py           Pembuat bank soal awal
supabase-schema.sql         SQL backend papan peringkat demo
tools/dev-server.mjs        Server pengembangan tanpa depedensi
tools/build.mjs             Static build tanpa depedensi
vercel.json                 Deploy configuration
```

**Lisensi:** Kode contoh untuk pembelajaran dan pengembangan lebih lanjut. Aset orisinal dalam proyek disediakan untuk digunakan bersama game ini.


## Rilis 1.2

Ditambahkan workflow GitHub Pages, `.gitignore`, dokumentasi deployment, dan pemeriksaan sintaks pada CI tanpa mengubah aturan game atau perbaikan tekstur versi 1.1.
