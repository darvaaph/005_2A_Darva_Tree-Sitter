# `cek.py` — Pemeriksa Kode Python Berbasis Tree-sitter

CLI kecil untuk memindai seluruh file `.py` di dalam suatu folder dan melaporkan tiga hal:
1. Komentar yang mengandung `TODO` atau `FIXME` (memakai query Tree-sitter dengan `#match?`).
2. Fungsi yang panjangnya lebih dari 30 baris (`end_point[0] - start_point[0] + 1 > 30`).
3. File yang mengandung syntax error (`tree.root_node.has_error`), beserta baris node `ERROR` atau `MISSING` pertama secara rekursif.

> **Catatan cakupan:** Pada fitur deteksi fungsi panjang, **semua fungsi ikut dihitung**, termasuk method di dalam `class` dan fungsi bersarang (*nested function*), karena semuanya diwakili oleh node `function_definition` pada grammar Python. Folder `.git/`, `venv/`, `.venv/`, `node_modules/`, dan `__pycache__/` otomatis dilewati.

## Cara Memasang Dependensi

```bash
pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan

```bash
python cek.py <folder_target>
```

Contoh menjalankan pada folder uji bawaan:

```bash
python cek.py uji
```

## Contoh Output

### 1. Uji pada folder `uji/` buatan sendiri
```text
[ERROR]   cek\uji\uji_error.py:1: ditemukan syntax error
[PANJANG] cek\uji\uji_panjang.py:5: fungsi 'fungsi_sangat_panjang' (33 baris)
[TODO]    cek\uji\uji_todo.py:1: # Contoh file dengan komentar TODO dan FIXME
[TODO]    cek\uji\uji_todo.py:4: # TODO: validasi input kosong sebelum diproses
[TODO]    cek\uji\uji_todo.py:7: # FIXME: tangani nilai None agar tidak crash
```

### 2. Uji pada repositori open source nyata (`https://github.com/tartley/colorama`)
```text
[PANJANG] ..\repo-uji-tmp\colorama\colorama\ansitowin32.py:81: fungsi '__init__' (39 baris)
[PANJANG] ..\repo-uji-tmp\colorama\colorama\ansitowin32.py:131: fungsi 'get_win32_calls' (43 baris)
[PANJANG] ..\repo-uji-tmp\colorama\colorama\tests\ansitowin32_test.py:240: fungsi 'test_native_windows_ansi' (43 baris)
[PANJANG] ..\repo-uji-tmp\colorama\colorama\tests\initialise_test.py:125: fungsi 'testJustFixWindowsConsole' (57 baris)
[PANJANG] ..\repo-uji-tmp\colorama\colorama\winterm.py:117: fungsi 'erase_screen' (31 baris)
```

### Verifikasi Manual pada 2 File Acak
1. `colorama/ansitowin32.py`:
   - `__init__` dimulai pada baris 81 dan berakhir pada baris 119 → `119 - 81 + 1 = 39` baris (cocok).
   - `get_win32_calls` dimulai pada baris 131 dan berakhir pada baris 173 → `173 - 131 + 1 = 43` baris (cocok).
2. `colorama/winterm.py`:
   - `erase_screen` dimulai pada baris 117 dan berakhir pada baris 147 → `147 - 117 + 1 = 31` baris (cocok).
