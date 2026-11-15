"""Mini App Penjualan – dashboard sederhana dari file Excel hasil Sesi 4.

Tanpa database dan tanpa login: aplikasi hanya membaca sheet "Data" dari laporan_penjualan.xlsx,
lalu menampilkan KPI, grafik, tabel yang bisa difilter, dan tombol download.

Cara menjalankan:
    - Online: unggah app.py, requirements.txt, dan laporan_penjualan.xlsx ke repo GitHub,
      lalu deploy di share.streamlit.io (main file: app.py).
    - Lokal, dari folder materi: streamlit run mini_app/app.py
"""
import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

FOLDER = Path(__file__).resolve().parent
# laporan_penjualan.xlsx di sebelah app.py (repo GitHub), atau di ../output (folder materi)
FILE_EXCEL = next((p for p in [FOLDER / "laporan_penjualan.xlsx", FOLDER.parent / "output" / "laporan_penjualan.xlsx"]
                   if p.exists()), FOLDER / "laporan_penjualan.xlsx")

st.set_page_config(page_title="Mini App Penjualan", page_icon="📊", layout="wide")


def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")


@st.cache_data
def baca_excel(sumber):
    """Baca sheet 'Data'. `sumber` boleh path file atau file yang diunggah."""
    df = pd.read_excel(sumber, sheet_name="Data")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df


# ------------------------------------------------------------------ sumber data
st.title("📊 Mini App Penjualan")
unggahan = st.file_uploader("Pakai file Excel sendiri (opsional)", type="xlsx",
                            help="Unggah laporan_penjualan.xlsx hasil notebook 04. Kosongkan untuk memakai data contoh.")
try:
    df = baca_excel(unggahan if unggahan else FILE_EXCEL)
except Exception as e:  # file salah / sheet "Data" tidak ada
    st.error(f"File tidak bisa dibaca: {e}. Pastikan ada sheet bernama Data.")
    st.stop()
st.caption(f"Sumber data: {unggahan.name if unggahan else FILE_EXCEL.name} · {len(df):,} baris".replace(",", "."))

# ------------------------------------------------------------------ filter
semua_cabang = sorted(df["cabang"].unique())
semua_bulan = sorted(df["bulan"].unique())
f1, f2 = st.columns(2)
cabang = f1.multiselect("Cabang", semua_cabang, default=semua_cabang)
dari, sampai = f2.select_slider("Periode", options=semua_bulan, value=(semua_bulan[0], semua_bulan[-1]))
df = df[df["cabang"].isin(cabang) & (df["bulan"] >= dari) & (df["bulan"] <= sampai)]
if df.empty:
    st.info("Tidak ada data untuk filter ini. Pilih minimal satu cabang.")
    st.stop()

# ------------------------------------------------------------------ ringkasan
k1, k2, k3 = st.columns(3)
k1.metric("Total penjualan", rupiah(df["total"].sum()))
k2.metric("Jumlah transaksi", f"{len(df):,}".replace(",", "."))
k3.metric("Rata-rata / transaksi", rupiah(df["total"].mean()))

kiri, kanan = st.columns(2)
per_bulan = df.groupby(["bulan", "cabang"], as_index=False)["total"].sum()
kiri.plotly_chart(px.line(per_bulan, x="bulan", y="total", color="cabang", markers=True, title="Tren bulanan"),
                  width="stretch")
per_kategori = df.groupby("kategori", as_index=False)["total"].sum().sort_values("total")
kanan.plotly_chart(px.bar(per_kategori, x="total", y="kategori", orientation="h", title="Per kategori"),
                   width="stretch")

# ------------------------------------------------------------------ tabel & download
st.subheader("Data transaksi")
cari = st.text_input("Cari nama produk")
tabel = df[df["nama_produk"].str.contains(cari, case=False, na=False)] if cari else df
st.dataframe(tabel, hide_index=True, width="stretch")

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    tabel.groupby("cabang", as_index=False)["total"].sum().to_excel(writer, sheet_name="Per Cabang", index=False)
    tabel.to_excel(writer, sheet_name="Data", index=False)
st.download_button("⬇️ Download Excel", buffer.getvalue(), file_name=f"penjualan_{dari}_{sampai}.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.download_button("⬇️ Download CSV", tabel.to_csv(index=False), file_name=f"penjualan_{dari}_{sampai}.csv",
                   mime="text/csv")
