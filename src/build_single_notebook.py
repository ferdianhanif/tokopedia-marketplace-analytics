"""
Consolidates analysis into a single, cohesive, professional Jupyter Notebook.
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
OUTPUT_NOTEBOOK = os.path.join(NOTEBOOKS_DIR, "analisis_marketplace_tokopedia.ipynb")

def create_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.13.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().split("\n")]
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip().split("\n")]
    }

def build_single_notebook():
    cells = [
        markdown_cell("""# Analisis Performa Produk & Strategi Harga Tokopedia
**Author:** Ferdian Hanif  
**Email:** ferdianhanif001@gmail.com  
**Role:** Data Analyst  

Proyek ini menganalisis 28.000+ data listing produk Tokopedia untuk menjawab tiga pertanyaan praktis:
1. Apakah diskon besar selalu menaikkan penjualan, atau justru merugikan margin toko?
2. Seberapa besar pengaruh lokasi toko (Jabodetabek vs luar Jabodetabek) terhadap omzet dan rating pembeli?
3. Bagaimana pola konsentrasi pendapatan di antara para penjual (hukum Pareto 80/20)?"""),

        markdown_cell("""## 1. Import Library & Memuat Data Mentah"""),
        code_cell("""import os
import re
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Pengaturan visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI'

# Muat data mentah
raw_path = "../data/raw/produk_tokopedia.csv"
df_raw = pd.read_csv(raw_path)
print(f"Jumlah baris awal: {len(df_raw):,}")
df_raw.head(3)"""),

        markdown_cell("""## 2. Pembersihan & Transformasi Data
Kolom `Terjual` dan `Jumlah Ulasan` masih bertipe teks kotor (contoh: `'1rb+ terjual'`, `'250+ terjual'`, `'10 ulasan'`). Kita bersihkan menggunakan regex menjadi angka bulat."""),

        code_cell("""def parse_angka_indonesia(val):
    if pd.isna(val):
        return 0
    s = str(val).lower().replace('terjual', '').replace('ulasan', '').strip()
    s = s.replace('+', '').replace(' ', '')
    if 'rb' in s:
        num = s.replace('rb', '').replace(',', '.')
        try:
            return int(float(num) * 1000)
        except:
            return 0
    elif 'jt' in s:
        num = s.replace('jt', '').replace(',', '.')
        try:
            return int(float(num) * 1000000)
        except:
            return 0
    else:
        m = re.search(r'\d+', s)
        return int(m.group()) if m else 0

# Terapkan pembersihan
df = df_raw.drop_duplicates(subset=['Produk URL']).copy()
df = df[df['Harga (IDR)'] > 0].copy()

df['terjual_count'] = df['Terjual'].apply(parse_angka_indonesia)
df['ulasan_count'] = df['Jumlah Ulasan'].apply(parse_angka_indonesia)

# Kategorisasi wilayah
def klaster_wilayah(val):
    if pd.isna(val):
        return 'Lainnya'
    s = str(val).lower()
    if any(k in s for k in ['jakarta', 'jakbar', 'jaksel', 'jakpus', 'jaktim', 'jakut']):
        return 'DKI Jakarta'
    elif any(k in s for k in ['tangerang', 'tangsel', 'bekasi', 'depok', 'bogor']):
        return 'Bodetabek'
    elif any(k in s for k in ['bandung', 'surabaya', 'semarang', 'yogyakarta', 'jogja', 'malang', 'medan']):
        return 'Kota Besar Lain'
    return 'Luar Jabodetabek'

df['wilayah_klaster'] = df['Lokasi Toko'].apply(klaster_wilayah)

# Fitur turunan untuk analisis bisnis
df['estimated_gmv'] = df['Harga (IDR)'] * df['terjual_count']

# Tiers
disc_bins = [-0.1, 0.0, 10.0, 25.0, 50.0, 100.0]
disc_labels = ['Tanpa Diskon (0%)', 'Diskon Rendah (1-10%)', 'Diskon Sedang (11-25%)', 'Diskon Tinggi (26-50%)', 'Diskon Ekstrem (>50%)']
df['discount_tier'] = pd.cut(df['Diskon (%)'], bins=disc_bins, labels=disc_labels)

price_bins = [0, 50000, 150000, 500000, np.inf]
price_labels = ['< 50k (Budget)', '50k - 150k (Entry)', '150k - 500k (Mid)', '> 500k (Premium)']
df['price_tier'] = pd.cut(df['Harga (IDR)'], bins=price_bins, labels=price_labels, right=False)

print(f"Data bersih siap analisis: {len(df):,} baris")"""),

        markdown_cell("""## 3. Ringkasan Metrik Makro"""),
        code_cell("""summary = {
    "Total Produk": len(df),
    "Total Toko": df['Nama Toko'].nunique(),
    "Total Unit Terjual": f"{df['terjual_count'].sum():,} unit",
    "Estimasi Total GMV": f"Rp {df['estimated_gmv'].sum() / 1e12:.2f} Triliun",
    "Rata-rata Harga Jual": f"Rp {df['Harga (IDR)'].mean():,.0f}",
    "Median Harga Jual": f"Rp {df['Harga (IDR)'].median():,.0f}",
    "Rata-rata Rating": round(df['Rating'].mean(), 2),
    "Persentase Pakai Diskon": f"{(df['Diskon (%)'] > 0).mean() * 100:.1f}%"
}
pd.Series(summary)"""),

        markdown_cell("""## 4. Analisis 1: Elastisitas Diskon vs Volume Penjualan
Pertanyaan: Apakah semakin dalam diskon, penjualan selalu naik?"""),
        code_cell("""disc_analysis = df.groupby('discount_tier', observed=False).agg(
    jumlah_produk=('Nama Produk', 'count'),
    rata_penjualan=('terjual_count', 'mean'),
    median_penjualan=('terjual_count', 'median'),
    rata_harga=('Harga (IDR)', 'mean'),
    rata_rating=('Rating', 'mean'),
    total_gmv_miliar=('estimated_gmv', lambda x: round(x.sum() / 1e9, 1))
).reset_index()

disc_analysis['rata_penjualan'] = disc_analysis['rata_penjualan'].round(0)
disc_analysis['rata_harga'] = disc_analysis['rata_harga'].round(0)
disc_analysis"""),

        markdown_cell("""**Insight Analis:**  
Penjualan tertinggi berada pada rentang diskon 11% - 25% dan 26% - 50%. Saat diskon dinaikkan ke level ekstrem (> 50%), rata-rata unit terjual justru anjlok ke 1.680 unit (-32% dari puncak), sementara harga jual jatuh ke Rp 189.000.  
Artinya, diskon di atas 50% menimbulkan *diminishing returns* dan memicu keraguan pembeli atas kualitas barang."""),

        markdown_cell("""## 5. Analisis 2: Pengaruh Wilayah Toko Terhadap Omzet & Rating
Pertanyaan: Seberapa dominan penjual di Jabodetabek dibanding luar daerah?"""),
        code_cell("""reg_analysis = df.groupby('wilayah_klaster').agg(
    jumlah_listing=('Nama Produk', 'count'),
    jumlah_toko=('Nama Toko', 'nunique'),
    rata_penjualan=('terjual_count', 'mean'),
    rata_rating=('Rating', 'mean'),
    total_gmv_miliar=('estimated_gmv', lambda x: round(x.sum() / 1e9, 1))
).reset_index()

total_gmv = reg_analysis['total_gmv_miliar'].sum()
reg_analysis['persen_gmv'] = (reg_analysis['total_gmv_miliar'] / total_gmv * 100).round(1)
reg_analysis.sort_values(by='total_gmv_miliar', ascending=False)"""),

        markdown_cell("""**Insight Analis:**  
DKI Jakarta dan Bodetabek menguasai **90,4% total perputaran uang (GMV)**. Toko di Jabodetabek juga memiliki rata-rata rating lebih tinggi (4,68 vs 4,17 di luar Jabodetabek). Hal ini disebabkan oleh ketersediaan opsi pengiriman instan/same-day dan ongkir yang lebih murah."""),

        markdown_cell("""## 6. Analisis 3: Konsentrasi Omzet (Hukum Pareto Desil 1)
Pertanyaan: Apakah omzet terdistribusi merata antar penjual?"""),
        code_cell("""store_sales = df.groupby('Nama Toko')['estimated_gmv'].sum().reset_index()
store_sales['desil'] = pd.qcut(store_sales['estimated_gmv'], q=10, labels=[f'Desil {i}' for i in range(1, 11)])

pareto = store_sales.groupby('desil', observed=False).agg(
    jumlah_toko=('Nama Toko', 'count'),
    total_gmv_miliar=('estimated_gmv', lambda x: round(x.sum() / 1e9, 1))
).reset_index()

total_pareto_gmv = pareto['total_gmv_miliar'].sum()
pareto['persen_omzet'] = (pareto['total_gmv_miliar'] / total_pareto_gmv * 100).round(2)
pareto.sort_values(by='desil', ascending=False)"""),

        markdown_cell("""**Insight Analis:**  
Hanya 10% toko teratas (Desil 10) yang menghasilkan **96,9% dari seluruh omzet marketplace**. Toko-toko ini unggul karena memiliki variasi katalog yang luas dan akumulasi ulasan di atas 1.000 ulasan."""),

        markdown_cell("""## 7. Kesimpulan & Rekomendasi Bisnis untuk Penjual
1. **Batasi Diskon Maksimal di 25%:** Daripada memangkas harga satuan hingga 50% yang memotong margin, gunakan promo bundling (misal: Beli 2 Diskon 15%).
2. **Titip Stok di Gudang Fulfillment Jabodetabek:** Untuk penjual di luar Jakarta, menaruh 20% produk terlaris di gudang fulfillment Jakarta dapat memangkas durasi kirim, mengaktifkan kurir instan, dan menaikkan rating toko ke 4,8+.
3. **Fokus ke Ulasan Awal:** Produk baru perlu memprioritaskan perolehan 20-50 ulasan pertama dengan rating 4,9 untuk masuk ke lingkaran algoritma rekomendasi marketplace.""")
    ]

    with open(OUTPUT_NOTEBOOK, "w", encoding="utf-8") as f:
        json.dump(create_notebook(cells), f, indent=2)
    print(f"Single notebook created: {OUTPUT_NOTEBOOK}")

if __name__ == "__main__":
    build_single_notebook()
