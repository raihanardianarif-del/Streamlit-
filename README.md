# Mini App Penjualan

Dashboard Streamlit sederhana dari file Excel: KPI, grafik tren dan kategori, tabel yang bisa difilter, serta download Excel/CSV. Tanpa database dan tanpa login.

## Isi repo
- `app.py`: kode aplikasi
- `requirements.txt`: library yang dipasang Streamlit Cloud
- `laporan_penjualan.xlsx`: data contoh (sheet `Data`), sama dengan hasil notebook 04

## Deploy
1. Unggah ketiga file di atas ke repo GitHub (Add file → Upload files → Commit changes).
2. Buka https://share.streamlit.io, masuk dengan akun GitHub, klik **Create app**.
3. Pilih repo ini, branch `main`, main file `app.py`, lalu **Deploy**.

## Pakai data sendiri
Di aplikasi, klik "Pakai file Excel sendiri" dan pilih `laporan_penjualan.xlsx` hasil notebook 04 (atau Excel lain yang punya sheet `Data` dengan kolom yang sama: tanggal, cabang, nama_produk, kategori, total, bulan).
