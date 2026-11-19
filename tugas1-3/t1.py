import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def parse_dan_cetak(judul, kode):
    """Parse potongan kode Python lalu cetak pohon S-expression dan status error."""
    tree = parser.parse(kode)
    root = tree.root_node
    print(f"=== {judul} (has_error={root.has_error}) ===")
    print(root)
    print()
    return tree


def cetak_anak(judul, node):
    """Cetak semua child node untuk membedakan node bernama dan node anonim."""
    print(f"=== {judul} ===")
    print(f"children={len(node.children)}, named_children={len(node.named_children)}")
    for c in node.children:
        status = "bernama" if c.is_named else "anonim"
        print(f"  {c.type!r:20} -> {status}")
    print()


parse_dan_cetak("Baseline", b"x = 1\n")

tree_fungsi = parse_dan_cetak(
    "Potongan 1: Fungsi",
    b"def luas(p, l):\n    return p * l\n",
)

parse_dan_cetak(
    "Potongan 2: if/else",
    b'if nilai >= 75:\n    status = "Lulus"\nelse:\n    status = "Remedial"\n',
)

parse_dan_cetak(
    "Potongan 3: Kelas dengan satu method",
    b"class Persegi:\n    def keliling(self, sisi):\n        return 4 * sisi\n",
)

fn_node = tree_fungsi.root_node.children[0]
cetak_anak("Node anak function_definition", fn_node)
cetak_anak("Node anak parameters", fn_node.child_by_field_name("parameters"))

parse_dan_cetak(
    "Error 1: Hapus ':' setelah parameter",
    b"def luas(p, l)\n    return p * l\n",
)

parse_dan_cetak(
    "Error 2: Hapus ')' setelah parameter",
    b"def luas(p, l:\n    return p * l\n",
)
