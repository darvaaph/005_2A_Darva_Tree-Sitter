import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah(node, kedalaman=0, field=None):
    """Cetak node bernama secara rekursif dengan indentasi, posisi, dan nama field."""
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    for i, child in enumerate(node.children):
        if not child.is_named:
            continue
        jelajah(child, kedalaman + 1, node.field_name_for_child(i))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Pemakaian: python jelajah.py <file.py>")
    with open(sys.argv[1], "rb") as f:
        tree = parser.parse(f.read())
    jelajah(tree.root_node)
