"""
High-Resolution Analytical Visualizations for Tokopedia Marketplace Study
Optimized for high legibility, large labels, and crisp executive presentation.
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from metrics import (
    get_connection,
    analyze_discount_elasticity,
    analyze_regional_performance,
    analyze_price_tier_performance,
    analyze_top_merchant_pareto
)

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "figures"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# High-contrast, large-font typography
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.labelweight": "bold",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "figure.titlesize": 14,
    "figure.titleweight": "bold",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.edgecolor": "#CBD5E1",
    "axes.linewidth": 1.2,
    "grid.color": "#F1F5F9",
    "grid.linestyle": "--",
    "grid.alpha": 0.9,
})

def plot_discount_elasticity(conn):
    """Figure 1: Average Units Sold by Discount Depth."""
    df = analyze_discount_elasticity(conn)
    tier_order = ["No Discount (0%)", "Low (1% - 10%)", "Medium (11% - 25%)", "High (26% - 50%)", "Deep (> 50%)"]
    tier_labels_id = ["Tanpa Diskon\n(0%)", "Rendah\n(1-10%)", "Sedang\n(11-25%)", "Tinggi\n(26-50%)", "Ekstrem\n(>50%)"]
    df["tier_cat"] = pd.Categorical(df["discount_tier"], categories=tier_order, ordered=True)
    df = df.sort_values("tier_cat")

    fig, ax = plt.subplots(figsize=(7.8, 5.2), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    colors = ["#64748B", "#3B82F6", "#2563EB", "#059669", "#D97706"]
    bars = ax.bar(tier_labels_id, df["avg_units_sold"], color=colors, width=0.55)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 90, f"{height:,.0f}",
                ha="center", va="bottom", fontsize=11, fontweight="bold", color="#0F172A")

    ax.set_ylim(0, max(df["avg_units_sold"]) * 1.18)
    ax.set_xlabel("Kedalaman Diskon Produk", labelpad=8)
    ax.set_ylabel("Rata-rata Unit Terjual per SKU", labelpad=8)
    ax.set_title("Kedalaman Diskon vs Volume: Titik Jenuh di atas 50%", pad=12)
    ax.grid(axis="y", visible=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig1_discount_elasticity_vs_volume.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_regional_distribution(conn):
    """Figure 2: Regional Hub Comparison (Listing Share vs GMV Share)."""
    df = analyze_regional_performance(conn).sort_values("total_gmv_billion_idr", ascending=True)

    fig, ax = plt.subplots(figsize=(7.8, 5.2), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    y = np.arange(len(df))
    height = 0.35

    total_gmv = df["total_gmv_billion_idr"].sum()
    df["gmv_pct"] = (df["total_gmv_billion_idr"] / total_gmv) * 100

    bars1 = ax.barh(y + height/2, df["share_pct"], height, label="Pangsa Listing Toko (%)", color="#94A3B8")
    bars2 = ax.barh(y - height/2, df["gmv_pct"], height, label="Pangsa Estimasi Nilai Transaksi (%)", color="#2563EB")

    ax.set_yticks(y)
    ax.set_yticklabels(df["wilayah_klaster"], fontweight="bold", fontsize=11)
    ax.set_xlabel("Persentase Pangsa Pasar (%)", labelpad=8)
    ax.set_title("Perbandingan Pangsa Listing vs Estimasi Nilai Transaksi", pad=12)
    ax.legend(loc="lower right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=10)
    ax.grid(axis="x", visible=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar in bars2:
        width = bar.get_width()
        ax.text(width + 1.2, bar.get_y() + bar.get_height()/2, f"{width:.1f}%",
                va="center", ha="left", fontsize=11, fontweight="bold", color="#1E40AF")

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig2_regional_gmv_and_merchant_share.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_price_tier_performance(conn):
    """Figure 3: Catalog Volume vs Total Revenue by Price Tier."""
    df = analyze_price_tier_performance(conn)
    tier_order = ["< 50k (Budget)", "50k - 150k (Entry)", "150k - 500k (Mid)", "> 500k (Premium)"]
    df["order"] = pd.Categorical(df["price_tier"], categories=tier_order, ordered=True)
    df = df.sort_values("order")

    fig, ax1 = plt.subplots(figsize=(8.0, 4.0), facecolor="#FFFFFF")
    ax1.set_facecolor("#FFFFFF")

    color1 = "#2563EB"
    color2 = "#059669"

    x = np.arange(len(df))
    width = 0.38

    bars = ax1.bar(x, df["catalog_share_pct"], width=width, color=color1, label="Pangsa Listing (%)")
    ax1.set_ylabel("Pangsa Listing Produk (%)", color=color1, labelpad=8)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df["price_tier"], fontweight="bold", fontsize=10)

    ax2 = ax1.twinx()
    total_gmv = df["total_gmv_billion_idr"].sum()
    gmv_share = (df["total_gmv_billion_idr"] / total_gmv) * 100
    line = ax2.plot(x, gmv_share, color=color2, marker="o", linewidth=2.5, markersize=8, label="Pangsa Nilai Transaksi (%)")
    ax2.set_ylabel("Pangsa Nilai Transaksi (%)", color=color2, labelpad=8)
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.grid(False)

    for i, txt in enumerate(gmv_share):
        ax2.annotate(f"{txt:.1f}%", (x[i], txt + 2.5), ha="center", fontsize=10, fontweight="bold", color=color2)

    ax1.set_title("Distribusi Jumlah Produk vs Nilai Transaksi per Tier Harga", pad=10)
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig3_price_tier_vs_gmv_contribution.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_merchant_pareto(conn):
    """Figure 4: Merchant Revenue Concentration (Pareto Curve)."""
    df = analyze_top_merchant_pareto(conn)

    fig, ax = plt.subplots(figsize=(8.0, 4.0), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    deciles = [f"D{d}" for d in df["decile_rank"]]
    colors = ["#DC2626" if d == 1 else "#CBD5E1" for d in df["decile_rank"]]

    bars = ax.bar(deciles, df["gmv_share_pct"], color=colors, width=0.6)

    for bar in bars:
        height = bar.get_height()
        if height > 0.5:
            ax.text(bar.get_x() + bar.get_width()/2, height + 1.8, f"{height:.1f}%",
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color="#0F172A")

    ax.set_ylim(0, 112)
    ax.set_xlabel("Kelompok Toko Berdasarkan Desil (D1: 10% Teratas)", labelpad=8)
    ax.set_ylabel("Pangsa Nilai Transaksi (%)", labelpad=8)
    ax.set_title("Distribusi Nilai Transaksi per Desil Toko", pad=10)
    ax.grid(axis="y", visible=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig4_merchant_pareto_concentration.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def main():
    conn = get_connection()
    print("Re-exporting optimized analytical figures...")
    plot_discount_elasticity(conn)
    plot_regional_distribution(conn)
    plot_price_tier_performance(conn)
    plot_merchant_pareto(conn)
    conn.close()
    print("All figures successfully exported.")

if __name__ == "__main__":
    main()
