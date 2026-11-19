# Laporan Penugasan Tree-sitter (PLP)

## 1. Tugas 1 – Membaca Pohon (`tugas1-3/t1.py`)
- **Penjelasan singkat:** Mem-parse tiga potongan kode Python (fungsi `luas`, `if/else`, dan `class Persegi` dengan satu method) serta mengecek perbedaan `children` vs `named_children` dan error recovery.
- **Perbandingan perkiraan vs hasil nyata:**
  - *Fungsi:* perkiraan awal `(module (function (name) (params) (return)))`; hasil asli memakai `function_definition` dengan field `name:`, `parameters:`, `body: (block (return_statement (binary_operator ...)))`.
  - *`if/else`:* awalnya diperkirakan nilai `"Lulus"` menjadi satu node `(string)`; ternyata grammar Python memecahnya menjadi `(string (string_start) (string_content) (string_end))` dan `if_statement` memakai field `condition:`, `consequence:`, serta `alternative: (else_clause ...)`.
  - *Kelas:* method di dalam `class_definition` ternyata tetap direpresentasikan sebagai `function_definition` biasa di dalam `block`.
- **Node bernama vs anonim (`children` vs `named_children`):** Pada `function_definition`, `children=5` sedangkan `named_children=3` karena token `'def'` dan `':'` bersifat anonim. Pada `parameters`, `children=5` sedangkan `named_children=2` karena `'('`, `','`, dan `')'` bersifat anonim (minimal 5 node anonim tersembunyi ditemukan).
- **Cuplikan output teks (`tugas1-3/hasil_t1.txt`):**
```text
=== Potongan 1: Fungsi (has_error=False) ===
(module (function_definition name: (identifier) parameters: (parameters (identifier) (identifier)) body: (block (return_statement (binary_operator left: (identifier) right: (identifier))))))

=== Node anak function_definition ===
children=5, named_children=3
  'def' -> anonim | 'identifier' -> bernama | 'parameters' -> bernama | ':' -> anonim | 'block' -> bernama

=== Node anak parameters ===
children=5, named_children=2
  '(' -> anonim | 'identifier' -> bernama | ',' -> anonim | 'identifier' -> bernama | ')' -> anonim

=== Error 1: Hapus ':' setelah parameter (has_error=True) ===
(module (ERROR (identifier) (parameters (identifier) (identifier)) (return_statement (binary_operator left: (identifier) right: (identifier)))))
```

## 2. Tugas 2 – Penjelajah Node (`tugas1-3/jelajah.py`)
- **Penjelasan singkat:** Skrip rekursif DFS preorder yang menelusuri `enumerate(node.children)`, melewati node yang `is_named == False`, lalu mengambil label peran memakai `node.field_name_for_child(i)` dengan indeks `node.children` (bukan `named_children`, agar label `field:` tidak hilang). Dijalankan pada `kecil.py` dan file tugas kuliah nyata `resolver.py` (190 baris → 1.293 baris output di `hasil_t2.txt`).
- **Cuplikan output teks (`kecil.py` & awal `hasil_t2.txt`):**
```text
# kecil.py
module [1:0]
  expression_statement [1:0]
    assignment [1:0]
      left: identifier [1:0]
      right: integer [1:4]

# resolver.py (190 baris, cuplikan awal)
import_from_statement [9:0]
  module_name: relative_import [9:5]
    import_prefix [9:5]
  name: aliased_import [9:14]
    name: dotted_name [9:14]
      identifier [9:14]
    alias: identifier [9:27]
```

## 3. Tugas 3 – Query Pertama (`tugas1-3/q.py` & `.scm`)
- **Penjelasan singkat:** Skrip `q.py` memakai `QueryCursor(...).matches(...)` agar dapat menjalankan empat file `.scm` (`semua.scm`, `fungsi.scm`, `print.scm`, `import.scm`) tanpa mengubah kode Python. Untuk `fungsi.scm`, `matches()` menjaga pasangan `@nama` dan `@params` lalu menghitung `params.named_child_count`. Untuk `import.scm`, struktur node diperiksa dulu memakai `jelajah.py` sehingga `import ... as ...` (`aliased_import`) dan `from ... import ...` ikut tertangkap.
- **Verifikasi manual pada `contoh_t3.py` (cocok 100%):** 4 fungsi (`salam` 0, `tambah` 2, `sapa_user` 2, `jalankan` 2), 5 panggilan `print(...)` (mengabaikan `len(data)`), dan 6 modul import (`os`, `sys`, `urllib.parse`, `pathlib`, `datetime`, `collections`).
- **Cuplikan output teks (`tugas1-3/hasil_t3.txt`):**
```text
=== Query: fungsi.scm (pada contoh_t3.py) ===
baris 9: salam (0 parameter)
baris 13: tambah (2 parameter)
baris 19: sapa_user (2 parameter)
baris 26: jalankan (2 parameter)

=== Query: print.scm (pada contoh_t3.py) ===
@fn  baris 10: print | @args  baris 10: ("Halo")  ... (total 5 panggilan: baris 10, 15, 21, 28, 34)

=== Query: import.scm (pada contoh_t3.py) ===
@modul baris 1: os | baris 2: sys | baris 3: urllib.parse | baris 4: pathlib | baris 5: datetime | baris 6: collections
```

## 4. Tugas 4 – Grammar DSL Filter (`tree-sitter-filter/`)
- **Penjelasan singkat:** Membangun grammar `filter` di `grammar.js` secara bertahap (4a–4f hingga `in_expression` dan `contains_expression`). Memasang `word: $ => $.identifier` agar keyword tidak tertukar dengan nama field, serta `prec(3)` (`not`), `prec.left(2)` (`and`), dan `prec.left(1)` (`or`) agar `a = 1 or b = 2 and c = 3` mengelompok menjadi `a = 1 or (b = 2 and c = 3)`. Ditambahkan 9 kasus uji di `test/corpus/dasar.txt`.
- **Output teks (`tree-sitter test`):**
```text
  dasar:
      1. ✓ perbandingan string dasar
      2. ✓ perbandingan angka dengan operator >=
      3. ✓ prioritas and lebih kuat dari or
      4. ✓ kurung mengubah urutan prioritas
      5. ✓ ekspresi not dan nilai boolean
      6. ✓ operator in dengan dua nilai
      7. ✓ operator in dengan tiga nilai
      8. ✓ operator contains untuk pencarian teks
      9. ✓ gabungan in, contains, and, or, not
Total parses: 9; successful parses: 9; failed parses: 0; success percentage: 100.00%
```

## 5. Tugas 5 – Highlight untuk DSL Filter (`queries/highlights.scm`)
- **Penjelasan singkat:** Menjalankan `tree-sitter init-config`, mendaftarkan folder induk `repo-tree-sitter` ke `parser-directories` di `config.json`, menambahkan `"highlights": "queries/highlights.scm"` di `tree-sitter.json`, serta menulis capture untuk `@keyword` (`and`, `or`, `not`, `in`, `contains`), `@operator`, `@string`, `@number`, `@constant.builtin` (`boolean`), dan `@property` (`field: (identifier)`).
- **Output teks (`tree-sitter query` & `tree-sitter highlight --html contoh.filter`):**
```text
<span class='keyword'>not</span> <span class='property'>archived</span> <span class='operator'>=</span> <span class='constant builtin'>true</span> <span class='keyword'>and</span> <span class='property'>status</span> <span class='keyword'>in</span> (<span class='string'>"open"</span>, <span class='string'>"pending"</span>, <span class='string'>"review"</span>) <span class='keyword'>and</span> (<span class='property'>priority</span> <span class='operator'>>=</span> <span class='number'>2</span> <span class='keyword'>or</span> <span class='property'>title</span> <span class='keyword'>contains</span> <span class='string'>"invoice"</span>)
```
Di terminal interaktif, `tree-sitter highlight contoh.filter` menampilkan warna ungu untuk keyword, merah untuk nama field, hijau untuk string, cokelat tebal untuk angka & boolean, dan abu-abu tebal untuk operator.

## 6. Tugas 6 – Mini Proyek `cek.py` (`cek/`)
- **Penjelasan singkat:** CLI `cek.py <folder>` yang memindai file `.py` (melewati `.git/`, `venv/`, `.venv/`, `node_modules/`, `__pycache__/`) untuk melaporkan komentar `TODO`/`FIXME`, fungsi >30 baris (semua fungsi termasuk method & fungsi bersarang ikut dihitung), dan file yang memiliki syntax error (`has_error`) beserta baris error pertamanya. Diuji pada folder `cek/uji/` dan repo open source `tartley/colorama`.
- **Verifikasi manual 2 file acak di `colorama`:** `colorama/ansitowin32.py` (`__init__` baris 81–119 = 39 baris; `get_win32_calls` baris 131–173 = 43 baris) dan `colorama/winterm.py` (`erase_screen` baris 117–147 = 31 baris) — keduanya cocok persis.
- **Output teks (`python cek/cek.py cek/uji` dan `colorama`):**
```text
[ERROR]   cek\uji\uji_error.py:1: ditemukan syntax error
[PANJANG] cek\uji\uji_panjang.py:5: fungsi 'fungsi_sangat_panjang' (33 baris)
[TODO]    cek\uji\uji_todo.py:4: # TODO: validasi input kosong sebelum diproses
[TODO]    cek\uji\uji_todo.py:7: # FIXME: tangani nilai None agar tidak crash
# Pada colorama: 5 fungsi >30 baris terdeteksi (ansitowin32.py:81 & 131, ansitowin32_test.py:240, initialise_test.py:125, winterm.py:117), 0 TODO/FIXME, 0 error.
```

## 7. Kendala dan Cara Mengatasinya
1. **`tree-sitter --version` tidak dikenali setelah `pip install`:** `pip install tree-sitter` hanya memasang binding Python, bukan CLI. *Solusi:* jalankan `npm install -g tree-sitter-cli`.
2. **`Unresolved conflict` di langkah 4c:** menambah `or_expression` tanpa `prec` memicu pesan konflik `_expr 'or' _expr • 'or'`. *Solusi:* gunakan `prec.left(1, ...)` pada `or_expression` dan `prec.left(2, ...)` pada `and_expression`.
3. **Salah paste antara `grammar.js` dan `contoh.filter`:** saat langkah 4a, isi JS tertukar ke `contoh.filter` sehingga `parse` memunculkan banyak `(ERROR ...)`. *Solusi:* kembalikan `contoh.filter` hanya berisi teks filter `priority >= 2` dan kode grammar ke `grammar.js`.
4. **Urutan `[TODO]` acak di `cek.py`:** `QueryCursor.captures()` sempat mencetak baris 1, 7, lalu 4. *Solusi:* urutkan capture dengan `sorted(..., key=lambda n: n.start_point)`.

## 8. Catatan Penggunaan AI
Saya menggunakan AI coding agent sebagai pendamping diskusi, penyusunan skrip, dan verifikasi bertahap untuk Tugas 1–6:
1. **Yang diminta ke AI:** Memandu pembuatan skrip `t1.py`, `jelajah.py`, `q.py`, `.scm`, `grammar.js`, `highlights.scm`, dan `cek.py` beserta penjelasan per langkahnya.
2. **Kesalahan / kekurangan AI yang ditemukan:**
   - Pada tahap setup Tugas 4, AI awalnya menyimpulkan laptop Windows saya tidak memiliki compiler C (karena `gcc`/`cl` tidak ada di `PATH`) dan menyarankan memakai WSL Ubuntu; padahal compiler MSVC `cl.exe` dari Visual Studio BuildTools sudah terpasang dan langsung ditemukan otomatis oleh `tree-sitter-cli`.
   - Pada Tugas 5, AI sempat memberikan perintah git yang salah ketik (`git add tree-sitter-json` memakai tanda hubung alih-alih titik).
   - Pada versi awal `cek.py` (Tugas 6), hasil tangkapan `[TODO]` keluar tidak urut per nomor baris.
3. **Cara membuktikannya:**
   - Menjalankan langsung `tree-sitter generate`, `tree-sitter parse contoh.filter`, dan `tree-sitter test` di PowerShell Windows hingga 9/9 tes lulus (membuktikan tidak perlu WSL).
   - Menjalankan perintah git di terminal memunculkan error `fatal: pathspec 'tree-sitter-json' did not match any files`, lalu diperbaiki ke `tree-sitter.json`.
   - Menjalankan `python cek/cek.py cek/uji` memperlihatkan output baris 1, 7, 4, lalu diuji ulang setelah ditambah `sorted(..., key=lambda n: n.start_point)` hingga urut menjadi 1, 4, 7.
