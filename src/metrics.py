"""
Marketplace Performance Metrics and Statistical Aggregations
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "tokopedia_marketplace.db")

def get_connection(db_path=DB_PATH):
    return sqlite3.connect(db_path)

def calculate_executive_kpis(conn):
    """Computes high-level marketplace summary KPIs."""
    query = """
    SELECT 
        COUNT(*) as total_listings,
        COUNT(DISTINCT [Nama Toko]) as total_merchants,
        ROUND(SUM(terjual_count) / 1000000.0, 2) as total_units_sold_million,
        ROUND(SUM(estimated_gmv_idr) / 1000000000.0, 2) as total_estimated_gmv_billion,
        ROUND(AVG(terjual_count), 1) as avg_units_sold,
        ROUND(AVG([Harga (IDR)]), 0) as avg_price_idr,
        ROUND(AVG([Rating]), 2) as avg_rating,
        ROUND(SUM(CASE WHEN [Diskon (%)] > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as discount_adoption_pct
    FROM tokopedia_products;
    """
    df = pd.read_sql_query(query, conn)
    return df.iloc[0].to_dict()

def analyze_discount_elasticity(conn):
    """
    Evaluates relationship between discount depth, sales volume, and rating.
    Answers: Does higher discount lead to higher sales volume?
    """
    query = """
    SELECT 
        discount_tier,
        COUNT(*) as total_products,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tokopedia_products), 1) as product_share_pct,
        ROUND(AVG(terjual_count), 1) as avg_units_sold,
        ROUND(AVG([Rating]), 2) as avg_rating,
        ROUND(AVG([Harga (IDR)]), 0) as avg_selling_price_idr,
        ROUND(SUM(estimated_gmv_idr) / 1000000000.0, 2) as gmv_billion_idr
    FROM tokopedia_products
    GROUP BY discount_tier
    ORDER BY avg_units_sold DESC;
    """
    return pd.read_sql_query(query, conn)

def analyze_price_tier_performance(conn):
    """Evaluates performance metrics across price brackets."""
    query = """
    SELECT 
        price_tier,
        COUNT(*) as product_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tokopedia_products), 1) as catalog_share_pct,
        ROUND(AVG(terjual_count), 1) as avg_units_sold,
        ROUND(AVG([Diskon (%)]), 1) as avg_discount_pct,
        ROUND(SUM(estimated_gmv_idr) / 1000000000.0, 2) as total_gmv_billion_idr
    FROM tokopedia_products
    GROUP BY price_tier
    ORDER BY total_gmv_billion_idr DESC;
    """
    return pd.read_sql_query(query, conn)

def analyze_regional_performance(conn):
    """Compares Jabodetabek vs Non-Jabodetabek merchant concentration."""
    query = """
    SELECT 
        wilayah_klaster,
        COUNT(*) as total_listings,
        COUNT(DISTINCT [Nama Toko]) as merchant_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tokopedia_products), 1) as share_pct,
        ROUND(AVG(terjual_count), 1) as avg_units_sold,
        ROUND(AVG([Rating]), 2) as avg_rating,
        ROUND(SUM(estimated_gmv_idr) / 1000000000.0, 2) as total_gmv_billion_idr
    FROM tokopedia_products
    GROUP BY wilayah_klaster
    ORDER BY total_gmv_billion_idr DESC;
    """
    return pd.read_sql_query(query, conn)

def analyze_rating_vs_sales(conn):
    """Analyzes sales volume based on customer review score."""
    query = """
    SELECT 
        rating_tier,
        COUNT(*) as listing_count,
        ROUND(AVG(terjual_count), 1) as avg_units_sold,
        ROUND(AVG(ulasan_count), 1) as avg_review_count,
        ROUND(AVG([Harga (IDR)]), 0) as avg_price_idr
    FROM tokopedia_products
    GROUP BY rating_tier
    ORDER BY avg_units_sold DESC;
    """
    return pd.read_sql_query(query, conn)

def analyze_top_merchant_pareto(conn):
    """Calculates GMV concentration (Pareto 80/20 rule) across merchants."""
    query = """
    WITH merchant_sales AS (
        SELECT 
            [Nama Toko] as store_name,
            wilayah_klaster,
            COUNT(*) as catalog_size,
            SUM(terjual_count) as total_units_sold,
            SUM(estimated_gmv_idr) as total_gmv
        FROM tokopedia_products
        GROUP BY [Nama Toko], wilayah_klaster
    ),
    ranked_merchants AS (
        SELECT 
            store_name,
            wilayah_klaster,
            catalog_size,
            total_units_sold,
            total_gmv,
            NTILE(10) OVER (ORDER BY total_gmv DESC) as decile_rank
        FROM merchant_sales
    )
    SELECT 
        decile_rank,
        COUNT(*) as merchant_count,
        ROUND(SUM(total_gmv) / 1000000000.0, 2) as decile_gmv_billion,
        ROUND(SUM(total_gmv) * 100.0 / (SELECT SUM(total_gmv) FROM ranked_merchants), 1) as gmv_share_pct
    FROM ranked_merchants
    GROUP BY decile_rank
    ORDER BY decile_rank ASC;
    """
    return pd.read_sql_query(query, conn)

if __name__ == "__main__":
    conn = get_connection()
    print("=== EXECUTIVE KPIS ===")
    print(calculate_executive_kpis(conn))
    print("\n=== DISCOUNT ELASTICITY ===")
    print(analyze_discount_elasticity(conn))
    print("\n=== REGIONAL HUBS ===")
    print(analyze_regional_performance(conn))
    print("\n=== TOP MERCHANT PARETO ===")
    print(analyze_top_merchant_pareto(conn))
    conn.close()
