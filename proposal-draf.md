# Draf Proposal Proyek Tree-sitter

## 1. Judul
**Guardrail Kualitas dan Keamanan Dasar Backend Express.js Berbasis Tree-sitter untuk Pipeline CI**

## 2. Masalah
Pada pengembangan backend aplikasi web enterprise berbasis Node.js/Express.js yang dikerjakan banyak developer, tiga kesalahan berulang sering lolos saat *code review*: (1) penggunaan `console.log` tertinggal di kode produksi alih-alih logger terstruktur, (2) penyusunan query database SQL dengan penggabungan string atau template literal `${...}` yang rawan SQL injection, dan (3) *route handler* asinkron (`app.get`/`router.post`) tanpa blok `try/catch` yang berisiko menyebabkan *unhandled rejection*. Pendekatan *regex* atau `grep` sering gagal karena memunculkan *false positive* pada komentar atau teks di dalam string, serta tidak mampu membaca struktur blok bersarang pada *route handler*.

## 3. Kenapa Tidak Cukup dengan AI Saja
Meminta AI melakukan *code review* di setiap *commit* memiliki hasil yang probabilistik (bisa berbeda antar-eksekusi), memakan biaya token berulang untuk ratusan file, dan relatif lambat dijalankan pada setiap *push*. Dengan memanfaatkan Tree-sitter, aturan pemeriksaan berjalan secara deterministik (hasil selalu konsisten untuk kode yang sama), berbiaya nol karena berjalan lokal, dan sangat cepat sehingga ideal dipasang otomatis sebagai *quality gate* di pipeline CI atau *pre-commit hook*, sementara AI cukup difokuskan pada perbaikan logika bisnis yang lebih kompleks.

## 4. Bahasa dan Framework Target
- **Bahasa & Framework:** JavaScript — Express.js (Node.js)
- **Grammar Tree-sitter:** `tree-sitter-javascript` (tersedia di PyPI)

## 5. Contoh Kode Target
- **Harus terdeteksi:**
```javascript
console.log("debug user:", req.body);
pool.query("SELECT * FROM users WHERE id = " + req.params.id);
pool.query(`SELECT * FROM orders WHERE code = ${code}`);
```
- **Tidak boleh ikut terdeteksi:**
```javascript
// console.log("jangan deteksi di komentar");
const info = "contoh teks console.log di string";
pool.query("SELECT * FROM users WHERE id = ?", [req.params.id]);
```

## 6. Rancangan Query (S-expression)
Aturan deteksi potensi SQL injection pada pemanggilan `.query(...)` yang memakai penggabungan string atau interpolasi template literal:
```scheme
(call_expression
  function: (member_expression
    property: (property_identifier) @method)
  arguments: (arguments
    [(binary_expression)
     (template_string (template_substitution))] @unsafe_arg)
  (#eq? @method "query"))
```

## 7. Bentuk Output
Laporan CLI di terminal (format `file:baris: [ATURAN] pesan`) dengan *exit code* non-nol jika ditemukan pelanggaran, serta opsi ekspor JSON agar mudah dibaca langkah CI (GitHub Actions).

## 8. Cara Evaluasi
- **Repositori uji:** Repositori Express.js open source di GitHub (misalnya `expressjs/express` folder `examples/` atau `hagopj13/node-express-boilerplate`) ditambah berkas uji buatan sendiri.
- **Metode pengecekan:** Mengambil sampel minimal 20 temuan dari hasil tool lalu mengecek secara manual berapa banyak temuan yang benar-benar merupakan pelanggaran nyata (*precision*) dan memeriksa 2 file secara menyeluruh untuk memastikan tidak ada kasus jelas yang terlewat.

## 9. Rencana Kerja dan Risiko
- **Minggu 1:** Finalisasi 3 aturan query (`console.log`, SQL concatenation/interpolation, `try/catch` pada route handler) dan uji pada kasus sintetik.
- **Minggu 2:** Bangun CLI Python pemindai folder + dukungan abaikan folder uji/komentar.
- **Minggu 3:** Tambahkan output JSON dan *exit code* CI serta integrasi GitHub Actions sederhana.
- **Minggu 4:** Pengujian dan evaluasi manual pada repositori Express.js open source nyata.
- **Minggu 5:** Perbaikan *false positive* dari hasil evaluasi, penulisan dokumentasi `README`, dan persiapan demo.
- **Risiko & mitigasi:** Variasi pola penulisan route/query (misal fungsi DB bernama selain `.query` atau template string tanpa substitusi); dimitigasi dengan menguji di repo nyata sejak awal dan membatasi skop hanya pada 3 aturan utama yang akurat.
