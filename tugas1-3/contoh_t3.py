import os
import sys as system
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter as Hitung


def salam():
    print("Halo")


def tambah(a, b):
    hasil = a + b
    print(hasil)
    return hasil


def sapa_user(nama, peran="mahasiswa"):
    teks = f"{nama} ({peran})"
    print(teks)
    return teks


class Penguji:
    def jalankan(self, data):
        jumlah = len(data)
        print("Selesai", jumlah)
        return jumlah


if __name__ == "__main__":
    salam()
    print("Mulai")
