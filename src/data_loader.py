"""
Data Cleaning and Feature Engineering Pipeline for Tokopedia Marketplace Analytics
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import re
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "produk_tokopedia.csv")
PROCESSED_CSV_PATH = os.path.join(BASE_DIR, "data", "processed", "clean_tokopedia_products.csv")
SQLITE_DB_PATH = os.path.join(BASE_DIR, "data", "processed", "tokopedia_marketplace.db")

def parse_count_string(val):
    """
    Parses messy marketplace count strings into numeric integers.
    Examples: '1rb+ terjual' -> 1000, '250+ terjual' -> 250, '10 ulasan' -> 10.
    """
    if pd.isna(val):
        return 0
    s = str(val).lower().replace("terjual", "").replace("ulasan", "").strip()
    s = s.replace("+", "").replace(" ", "")
    
    if "rb" in s:
        num = s.replace("rb", "").replace(",", ".")
        try:
            return int(float(num) * 1000)
        except (ValueError, TypeError):
            return 0
    elif "jt" in s:
        num = s.replace("jt", "").replace(",", ".")
        try:
            return int(float(num) * 1000000)
        except (ValueError, TypeError):
            return 0
    else:
        m = re.search(r"\d+", s)
        return int(m.group()) if m else 0

def categorize_location(val):
    """Standardizes store locations into high-level economic clusters."""
    if pd.isna(val):
        return "Unknown / Tidak Disebutkan"
    s = str(val).strip()
    s_lower = s.lower()
    
    if any(k in s_lower for k in ["jakarta", "jakbar", "jaksel", "jakpus", "jaktim", "jakut"]):
        return "DKI Jakarta"
    elif any(k in s_lower for k in ["tangerang", "tangsel", "bekasi", "depok", "bogor"]):
        return "Bodetabek"
    elif any(k in s_lower for k in ["bandung", "surabaya", "semarang", "yogyakarta", "jogja", "solo", "surakarta", "malang", "medan"]):
        return "Kota Besar Lainnya"
    else:
        return "Luar Jabodetabek"

def clean_tokopedia_data(input_path=RAW_PATH):
    """Loads, cleans, transforms, and engineers features for Tokopedia listings."""
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    
    # 1. Deduplicate by Produk URL
    df = df.drop_duplicates(subset=["Produk URL"], keep="first").copy()
    dedup_rows = initial_rows - len(df)
    print(f"Deduplication: removed {dedup_rows} duplicate product URLs.")
    
    # 2. Filter out invalid/zero prices
    valid_price_mask = df["Harga (IDR)"] > 0
    df = df[valid_price_mask].copy()
    
    # 3. Parse units sold and review counts
    df["terjual_count"] = df["Terjual"].apply(parse_count_string)
    df["ulasan_count"] = df["Jumlah Ulasan"].apply(parse_count_string)
    
    # 4. Standardize text features
    df["Nama Produk"] = df["Nama Produk"].astype(str).str.strip()
    df["Nama Toko"] = df["Nama Toko"].fillna("Toko Tanpa Nama").astype(str).str.strip()
    df["Lokasi Toko"] = df["Lokasi Toko"].fillna("Tidak Disebutkan").astype(str).str.strip()
    
    # 5. Location clustering
    df["wilayah_klaster"] = df["Lokasi Toko"].apply(categorize_location)
    df["is_jabodetabek"] = df["wilayah_klaster"].isin(["DKI Jakarta", "Bodetabek"]).astype(int)
    
    # 6. Feature Engineering
    # A. Estimated GMV (Proxy: Harga * Terjual)
    df["estimated_gmv_idr"] = df["Harga (IDR)"] * df["terjual_count"]
    
    # B. Original price before discount
    has_discount = df["Diskon (%)"] > 0
    df["original_price_idr"] = df["Harga (IDR)"]
    df.loc[has_discount, "original_price_idr"] = (
        df.loc[has_discount, "Harga (IDR)"] / (1 - (df.loc[has_discount, "Diskon (%)"] / 100.0))
    ).round(0)
    df["discount_amount_idr"] = df["original_price_idr"] - df["Harga (IDR)"]
    
    # C. Price Tiers
    price_bins = [0, 50000, 150000, 500000, np.inf]
    price_labels = ["< 50k (Budget)", "50k - 150k (Entry)", "150k - 500k (Mid)", "> 500k (Premium)"]
    df["price_tier"] = pd.cut(df["Harga (IDR)"], bins=price_bins, labels=price_labels, right=False)
    
    # D. Discount Tiers
    disc_bins = [-0.1, 0.0, 10.0, 25.0, 50.0, 100.0]
    disc_labels = ["No Discount (0%)", "Low (1% - 10%)", "Medium (11% - 25%)", "High (26% - 50%)", "Deep (> 50%)"]
    df["discount_tier"] = pd.cut(df["Diskon (%)"], bins=disc_bins, labels=disc_labels)
    
    # E. Rating Tiers
    rating_bins = [-0.1, 0.1, 4.4, 4.7, 4.9, 5.0]
    rating_labels = ["Unrated (0.0)", "Low (< 4.5)", "Good (4.5 - 4.7)", "High (4.8 - 4.9)", "Perfect (5.0)"]
    df["rating_tier"] = pd.cut(df["Rating"], bins=rating_bins, labels=rating_labels)
    
    # F. Review conversion proxy: ulasan per penjualan
    df["review_rate"] = np.where(
        df["terjual_count"] > 0,
        (df["ulasan_count"] / df["terjual_count"]).clip(0, 1.0),
        0.0
    ).round(3)
    
    print(f"Data cleaning complete: {len(df)} verified rows.")
    return df

def save_to_csv_and_sqlite(df, csv_path=PROCESSED_CSV_PATH, db_path=SQLITE_DB_PATH):
    """Persists cleaned data to CSV and SQLite relational database."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Saved processed CSV: {csv_path}")
    
    conn = sqlite3.connect(db_path)
    df.to_sql("tokopedia_products", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print(f"Saved SQLite database: {db_path} (table: tokopedia_products)")

if __name__ == "__main__":
    clean_df = clean_tokopedia_data()
    save_to_csv_and_sqlite(clean_df)
