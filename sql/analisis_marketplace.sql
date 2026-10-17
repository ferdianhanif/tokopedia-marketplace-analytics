-- ====================================================================
-- Portofolio Analisis Data Marketplace Tokopedia
-- Berkas Tunggal Kueri SQL Terpadu (Single Consolidated SQL File)
-- 
-- Author : Ferdian Hanif
-- Email  : ferdianhanif001@gmail.com
-- Dialek : ANSI SQL (Kompatibel langsung dengan PostgreSQL, MySQL 8.0+, dan SQLite)
-- Tabel  : tokopedia_products (28.704 baris produk tervalidasi dari 14.128 toko)
-- ====================================================================


-- --------------------------------------------------------------------
-- BAGIAN 1: RINGKASAN METRIK & KPI KATALOG MARKETPLACE
-- --------------------------------------------------------------------

-- 1.1 Metrik Agregat Eksekutif (Marketplace Overview KPIs)
SELECT 
    COUNT(*) AS total_catalog_listings,
    COUNT(DISTINCT "Nama Toko") AS active_merchant_count,
    ROUND(SUM(terjual_count) / 1000000.0, 2) AS total_units_sold_million,
    ROUND(SUM(estimated_gmv_idr) / 1000000000.0, 2) AS total_estimated_gmv_billion_idr,
    ROUND(AVG(terjual_count), 1) AS avg_units_sold_per_product,
    ROUND(AVG("Harga (IDR)"), 0) AS avg_listed_price_idr,
    ROUND(AVG("Rating"), 2) AS avg_marketplace_rating,
    ROUND(SUM(CASE WHEN "Diskon (%)" > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS discount_penetration_rate_pct
FROM tokopedia_products;


-- --------------------------------------------------------------------
-- BAGIAN 2: ANALISIS ELASTISITAS DISKON & SENSITIVITAS VOLUME
-- --------------------------------------------------------------------

-- 2.1 Evaluasi Volume Penjualan, Rating, dan Nilai GMV per Rentang Diskon
WITH discount_cohorts AS (
    SELECT 
        discount_tier,
        terjual_count,
        ulasan_count,
        "Rating" AS rating,
        "Harga (IDR)" AS selling_price,
        estimated_gmv_idr
    FROM tokopedia_products
)
SELECT 
    discount_tier,
    COUNT(*) AS total_products,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM discount_cohorts), 1) AS catalog_share_pct,
    ROUND(AVG(terjual_count), 1) AS avg_units_sold,
    ROUND(AVG(rating), 2) AS avg_customer_rating,
    ROUND(AVG(selling_price), 0) AS avg_price_idr,
    ROUND(SUM(estimated_gmv_idr) / 1000000000.0, 2) AS total_gmv_billion_idr,
    ROUND(AVG(ulasan_count), 1) AS avg_reviews_count
FROM discount_cohorts
GROUP BY discount_tier
ORDER BY avg_units_sold DESC;


-- --------------------------------------------------------------------
-- BAGIAN 3: ANALISIS KONSENTRASI OMZET TOKO (DISTRIBUSI DESIL PARETO)
-- --------------------------------------------------------------------

-- 3.1 Evaluasi Konsolidasi Omzet Toko Berdasarkan Peringkat Desil (NTILE 10)
WITH merchant_aggregates AS (
    SELECT 
        "Nama Toko" AS store_name,
        wilayah_klaster,
        COUNT(*) AS total_skus,
        SUM(terjual_count) AS total_units_sold,
        SUM(estimated_gmv_idr) AS store_gmv_idr
    FROM tokopedia_products
    GROUP BY "Nama Toko", wilayah_klaster
),
ranked_merchants AS (
    SELECT 
        store_name,
        wilayah_klaster,
        total_skus,
        total_units_sold,
        store_gmv_idr,
        NTILE(10) OVER (ORDER BY store_gmv_idr DESC) AS decile_rank
    FROM merchant_aggregates
)
SELECT 
    decile_rank,
    COUNT(*) AS merchant_count,
    ROUND(SUM(store_gmv_idr) / 1000000000.0, 2) AS decile_gmv_billion_idr,
    ROUND(SUM(store_gmv_idr) * 100.0 / (SELECT SUM(store_gmv_idr) FROM ranked_merchants), 2) AS gmv_share_pct,
    ROUND(AVG(total_units_sold), 1) AS avg_merchant_units_sold,
    ROUND(AVG(total_skus), 1) AS avg_skus_per_merchant
FROM ranked_merchants
GROUP BY decile_rank
ORDER BY decile_rank ASC;
