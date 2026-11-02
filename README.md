# Math Adventure: Fraction Kingdom v1.3 — NO BUILD

**Versi ini khusus untuk deployment langsung dari GitHub ke Vercel atau GitHub Pages.** Game telah menjadi static HTML/CSS/JavaScript; **jangan jalankan `npm run build`**. Tidak ada `package.json` ataupun dependency NPM.

## File yang wajib ada pada ROOT repo GitHub

- `index.html`, `styles.css`, `config.js`, `questions.json`, `vercel.json`
- Folder `assets/`, `src/`, `.github/workflows/`

> Upload seluruh **isi folder ekstraksi**, bukan ZIP dan bukan folder pembungkusnya.

## Vercel (web only)

1. Di GitHub unggah isi paket ini ke **root** repository game (branch `main`). Bila ada file lama dari versi 1.2, hapus `package.json`, folder `public/`, `tools/`, dan `dist/` lama agar proyek jelas hanya memakai versi statis ini.
2. Vercel → Project → Settings → Build and Deployment → Framework Preset: **Other**; Root Directory: **./** (root). Build Command: aktifkan Override dan **kosongkan**. Output Directory: `.` (titik). Simpan.
3. `vercel.json` dalam paket juga mengatur `buildCommand: null`, `framework: null`, `outputDirectory: "."`.
4. Pada Deployments pilih `Redeploy` **tanpa memakai Build Cache**, atau push commit baru dari GitHub.
5. Periksa log deployment menampilkan proses tanpa `npm run build`, kemudian kunjungi URL `.vercel.app`.

## GitHub Pages (web only)

1. Di GitHub repo → Settings → Pages → Source **GitHub Actions**.
2. Workflow `.github/workflows/deploy-pages.yml` menerbitkan game setelah commit ke branch main; workflow tidak menjalankan `npm install` atau `npm run build`.
3. Setelah Actions berhasil, game terbuka pada `https://USERNAME.github.io/REPOSITORY/`.

## Test setelah game online

- Halaman utama tampil; tombol Mulai berfungsi.
- Karakter bergerak dengan panah/A-D, lompat menggunakan Space.
- Kotak pertanyaan dapat dibuka; 4 opsi jawaban tampil dan skor/combo berubah.
- Halaman Hall of Fame dapat dibuka dan skor bisa disimpan lokal.
- Periksa DevTools → Console atau Network jika ada asset 404.

**Hall of Fame belum global:** papan skor antar-perangkat memerlukan konfigurasi backend Supabase. Secara default skor tersimpan pada browser tiap siswa.

Game dan seluruh aset bersumber dari Math Adventure v1.2 yang telah dibangun, tanpa perubahan mekanik permainan.
