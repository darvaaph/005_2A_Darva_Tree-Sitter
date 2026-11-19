import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")
SKIP_DIRS = {".git", "venv", ".venv", "node_modules", "__pycache__"}
BATAS_BARIS = 30


def cari_error_pertama(node):
    """Kembalikan node pertama yang is_error atau is_missing secara DFS."""
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        err = cari_error_pertama(child)
        if err is not None:
            return err
    return None


def cek_file(path):
    """Periksa satu file Python untuk TODO/FIXME, fungsi panjang, dan syntax error."""
    tree = parser.parse(path.read_bytes())
    root = tree.root_node

    # Fitur 1: komentar TODO/FIXME
    for node in sorted(
        QueryCursor(Q_TODO).captures(root).get("c", []),
        key=lambda n: n.start_point,
    ):
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO]    {path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi dengan panjang > 30 baris (semua fungsi: top-level, method, nested)
    for _, cap in QueryCursor(Q_FUNGSI).matches(root):
        fn_nodes = cap.get("fungsi", [])
        nama_nodes = cap.get("nama", [])
        if not fn_nodes or not nama_nodes:
            continue
        fn = fn_nodes[0]
        nama = nama_nodes[0].text.decode(errors="replace")
        jumlah_baris = fn.end_point[0] - fn.start_point[0] + 1
        if jumlah_baris > BATAS_BARIS:
            print(f"[PANJANG] {path}:{fn.start_point[0] + 1}: fungsi '{nama}' ({jumlah_baris} baris)")

    # Fitur 3: file yang pohonnya mengandung syntax error
    if root.has_error:
        err = cari_error_pertama(root)
        baris = err.start_point[0] + 1 if err is not None else "?"
        print(f"[ERROR]   {path}:{baris}: ditemukan syntax error")


def main():
    if len(sys.argv) < 2:
        sys.exit("Pemakaian: python cek.py <folder>")

    target = Path(sys.argv[1])
    if not target.exists():
        sys.exit(f"Folder tidak ditemukan: {target}")

    files = [target] if target.is_file() else sorted(target.rglob("*.py"))
    for path in files:
        if SKIP_DIRS & set(path.parts):
            continue
        cek_file(path)


if __name__ == "__main__":
    main()
