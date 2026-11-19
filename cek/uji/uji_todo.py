# Contoh file dengan komentar TODO dan FIXME

def proses_data(items):
    # TODO: validasi input kosong sebelum diproses
    hasil = []
    for item in items:
        # FIXME: tangani nilai None agar tidak crash
        hasil.append(item)
    return hasil
