import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)


def jalankan_query(path_kode, path_pola):
    """Parse file Python lalu jalankan query Tree-sitter dari file .scm."""
    kode = Path(path_kode).read_bytes()
    pola = Path(path_pola).read_text(encoding="utf-8")
    tree = parser.parse(kode)

    matches = QueryCursor(Query(PY, pola)).matches(tree.root_node)
    for _, cap in matches:
        if "nama" in cap and "params" in cap:
            fn = cap["nama"][0]
            params = cap["params"][0]
            nama_fn = fn.text.decode(errors="replace")
            print(f"baris {fn.start_point[0] + 1}: {nama_fn} ({params.named_child_count} parameter)")
            continue

        for label, nodes in cap.items():
            for n in nodes:
                teks = n.text.decode(errors="replace")
                print(f"@{label}  baris {n.start_point[0] + 1}: {teks}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Pemakaian: python q.py <file.py> <pola.scm>")
    jalankan_query(sys.argv[1], sys.argv[2])
