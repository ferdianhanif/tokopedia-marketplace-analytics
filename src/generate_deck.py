"""
Executive Presentation Deck Generator for Tokopedia Marketplace Analytics
Clean, professional, pixel-perfect 16:9 Landscape presentation deck.
Exact styling match for 'AWS Cloud Engineering Labs - Ferdian Hanif (ID).pdf':
- Canvas: 1080pt x 607.92pt (exact 16:9)
- Warm cream background (#FAF9F5)
- Title: Barlow Condensed ExtraBold (#4361EE), font-size 38pt - 45pt
- Subtitle: Inter Bold uppercase green (#059669), font-size 15.5pt - 16pt
- Body & Bullets: Inter, font-size 15pt - 15.5pt, line-height 1.55
- Crisp White Cards with high-res figures & centered captions
- Cover slide with concentric rings on left and wavy contour lines on bottom right
- Pill badge on cover: Ferdian Hanif & ferdianhanif001@gmail.com (NO DEGREES)
- Slide 6: Strategy Cards + Terminal Diagnostic Bar matching AWS Slide 10
- 100% natural Indonesian using humanizer principles (Junior-to-Mid Data Analyst POV)
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HTML_TEMPLATE_PATH = os.path.join(BASE_DIR, "reports", "deck_template.html")
PDF_OUTPUT_PATH = os.path.join(BASE_DIR, "reports", "presentation_deck.pdf")
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")

def get_file_uri(filename):
    path = os.path.join(FIG_DIR, filename).replace("\\", "/")
    return f"file:///{path}"

FIG1_URI = get_file_uri("fig1_discount_elasticity_vs_volume.png")
FIG2_URI = get_file_uri("fig2_regional_gmv_and_merchant_share.png")
FIG3_URI = get_file_uri("fig3_price_tier_vs_gmv_contribution.png")
FIG4_URI = get_file_uri("fig4_merchant_pareto_concentration.png")

# Corner graphics
CONTOUR_BOTTOM_LEFT = """
<svg class="contour-svg bottom-left" viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M-60 460 C 40 370, 160 480, 240 390 C 320 300, 190 170, 300 70" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M-80 480 C 30 380, 150 490, 250 400 C 340 310, 200 160, 320 60" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M-100 500 C 20 390, 140 500, 260 410 C 360 320, 210 150, 340 50" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M-120 520 C 10 400, 130 510, 270 420 C 380 330, 220 140, 360 40" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M-140 540 C 0 410, 120 520, 280 430 C 400 340, 230 130, 380 30" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M-160 560 C -10 420, 110 530, 290 440 C 420 350, 240 120, 400 20" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

CONTOUR_BOTTOM_RIGHT = """
<svg class="contour-svg bottom-right" viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M220 480 C 290 390, 390 470, 460 380 C 530 290, 410 170, 520 90" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M200 500 C 280 400, 380 480, 470 390 C 550 300, 420 160, 540 80" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M180 520 C 270 410, 370 490, 480 400 C 570 310, 430 150, 560 70" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M160 540 C 260 420, 360 500, 490 410 C 590 320, 440 140, 580 60" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
  <path d="M140 560 C 250 430, 350 510, 500 420 C 610 330, 450 130, 600 50" stroke="#93C5FD" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

RINGS_TOP_LEFT = """
<svg class="contour-svg top-left" viewBox="0 0 300 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="10" cy="110" r="105" stroke="#93C5FD" stroke-width="1.8"/>
  <circle cx="10" cy="170" r="105" stroke="#93C5FD" stroke-width="1.8"/>
  <circle cx="10" cy="230" r="105" stroke="#93C5FD" stroke-width="1.8"/>
  <circle cx="10" cy="290" r="105" stroke="#93C5FD" stroke-width="1.8"/>
  <circle cx="10" cy="350" r="105" stroke="#93C5FD" stroke-width="1.8"/>
</svg>
"""

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  @page {{
    size: 1080pt 607.92pt;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1E293B;
    background-color: #FAF9F5;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .slide {{
    width: 1080pt;
    height: 607.92pt;
    padding: 34pt 52pt 28pt 52pt;
    page-break-after: always;
    position: relative;
    background-color: #FAF9F5;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}

  /* Background SVGs */
  .contour-svg {{
    position: absolute;
    pointer-events: none;
    z-index: 1;
    opacity: 0.75;
  }}
  .contour-svg.bottom-left {{
    width: 280pt;
    height: 280pt;
    bottom: -30pt;
    left: -30pt;
  }}
  .contour-svg.bottom-right {{
    width: 280pt;
    height: 280pt;
    bottom: -25pt;
    right: -25pt;
  }}
  .contour-svg.top-left {{
    width: 200pt;
    height: 320pt;
    top: 30pt;
    left: -25pt;
  }}

  /* Content Wrapper */
  .content-layer {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    height: 100%;
  }}

  /* Slide Header */
  .slide-header {{
    text-align: center;
    margin-bottom: 22pt;
  }}
  .slide-title {{
    font-family: 'Barlow Condensed', 'Impact', sans-serif;
    font-size: 38pt;
    font-weight: 800;
    letter-spacing: 0.8pt;
    text-transform: uppercase;
    color: #4361EE;
    line-height: 1.1;
    margin-bottom: 4pt;
  }}
  .slide-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 15.5pt;
    font-weight: 700;
    letter-spacing: 1.4pt;
    text-transform: uppercase;
    color: #059669;
  }}

  /* 2-Column Grid Layout */
  .grid-2 {{
    display: grid;
    grid-template-columns: 505pt 450pt;
    gap: 20pt;
    align-items: center;
    flex: 1;
  }}

  /* Bullets & Typography */
  .bullet-list {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}
  .bullet-list > li {{
    font-size: 14.8pt;
    line-height: 1.55;
    color: #1E293B;
    margin-bottom: 14pt;
    position: relative;
    padding-left: 22pt;
  }}
  .bullet-list > li:last-child {{
    margin-bottom: 0;
  }}
  .bullet-list > li::before {{
    content: "•";
    color: #0F172A;
    font-size: 20pt;
    position: absolute;
    left: 0;
    top: -3pt;
    font-weight: bold;
  }}
  .bullet-list strong {{
    color: #0F172A;
    font-weight: 700;
  }}
  .sub-bullet-list {{
    list-style: none;
    margin-top: 5pt;
    margin-left: 4pt;
  }}
  .sub-bullet-list li {{
    font-size: 13.8pt;
    line-height: 1.5;
    color: #334155;
    margin-bottom: 5pt;
    position: relative;
    padding-left: 18pt;
  }}
  .sub-bullet-list li:last-child {{
    margin-bottom: 0;
  }}
  .sub-bullet-list li::before {{
    content: "○";
    color: #4361EE;
    font-size: 12pt;
    position: absolute;
    left: 0;
    top: 0;
    font-weight: bold;
  }}

  /* White Card Containers */
  .chart-card-single {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12pt;
    padding: 10pt;
    box-shadow: 0 4pt 12pt rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
  }}
  .chart-card-single img {{
    width: 100%;
    height: 330pt;
    object-fit: contain;
    border-radius: 6pt;
  }}
  .chart-card-caption {{
    font-size: 13.5pt;
    font-weight: 700;
    color: #0F172A;
    text-align: center;
    margin-top: 8pt;
  }}

  /* Stacked Half Cards (Slide 5) */
  .card-stack {{
    display: flex;
    flex-direction: column;
    gap: 12pt;
    width: 100%;
  }}
  .chart-card-half {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10pt;
    padding: 8pt 10pt 6pt 10pt;
    box-shadow: 0 3pt 8pt rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .chart-card-half img {{
    width: 100%;
    height: 148pt;
    object-fit: contain;
    border-radius: 4pt;
  }}
  .chart-card-half .caption {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #0F172A;
    text-align: center;
    margin-top: 4pt;
  }}

  /* Slide 2 Macro KPI Cards */
  .kpi-container {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12pt;
    padding: 16pt;
    box-shadow: 0 4pt 12pt rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12pt;
    margin-bottom: 12pt;
  }}
  .kpi-box {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 4pt solid #2563EB;
    border-radius: 8pt;
    padding: 12pt 14pt;
  }}
  .kpi-box.green {{
    border-left-color: #059669;
  }}
  .kpi-box.amber {{
    border-left-color: #D97706;
  }}
  .kpi-box.purple {{
    border-left-color: #7C3AED;
  }}
  .kpi-label {{
    font-size: 11pt;
    font-weight: 700;
    letter-spacing: 0.8pt;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 3pt;
  }}
  .kpi-val {{
    font-size: 24pt;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
    margin-bottom: 3pt;
  }}
  .kpi-desc {{
    font-size: 10.5pt;
    color: #475569;
  }}
  .kpi-highlight {{
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 8pt;
    padding: 10pt 14pt;
    font-size: 11.5pt;
    color: #1E3A8A;
    line-height: 1.5;
  }}

  /* Slide 6 Strategic Cards (matching AWS Slide 10) */
  .strategy-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18pt;
    margin-bottom: 16pt;
  }}
  .strategy-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12pt;
    padding: 18pt 20pt;
    box-shadow: 0 4pt 12pt rgba(0, 0, 0, 0.03);
  }}
  .strategy-card-title {{
    font-size: 15.5pt;
    font-weight: 800;
    letter-spacing: 0.5pt;
    text-transform: uppercase;
    margin-bottom: 12pt;
  }}
  .strategy-card-title.pricing {{
    color: #4361EE;
  }}
  .strategy-card-title.logistics {{
    color: #059669;
  }}
  .strategy-bullets {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}
  .strategy-bullets li {{
    font-size: 13.5pt;
    line-height: 1.5;
    color: #334155;
    margin-bottom: 9pt;
    position: relative;
    padding-left: 18pt;
  }}
  .strategy-bullets li:last-child {{
    margin-bottom: 0;
  }}
  .strategy-bullets li::before {{
    content: "•";
    color: #0F172A;
    font-size: 18pt;
    position: absolute;
    left: 0;
    top: -3pt;
    font-weight: bold;
  }}
  .strategy-bullets strong {{
    color: #0F172A;
  }}
  .diagnostic-terminal {{
    background: #0F172A;
    border-radius: 8pt;
    padding: 12pt 18pt;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    color: #F8FAFC;
    font-size: 11.5pt;
    line-height: 1.6;
  }}
  .diagnostic-terminal .term-title {{
    color: #10B981;
    font-weight: 700;
    margin-bottom: 4pt;
  }}
  .diagnostic-terminal .term-line {{
    color: #CBD5E1;
  }}
  .diagnostic-terminal .term-highlight {{
    color: #FBBF24;
    font-weight: 700;
  }}

  /* Cover Slide Layout */
  .cover-box {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
  }}
  .cover-title {{
    font-family: 'Barlow Condensed', 'Impact', sans-serif;
    font-size: 45pt;
    font-weight: 800;
    letter-spacing: 1.2pt;
    text-transform: uppercase;
    color: #4361EE;
    line-height: 1.15;
    max-width: 820pt;
    margin-bottom: 14pt;
  }}
  .cover-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 15.5pt;
    font-weight: 600;
    color: #475569;
    letter-spacing: 1.2pt;
    text-transform: uppercase;
    max-width: 780pt;
    line-height: 1.5;
    margin-bottom: 32pt;
  }}
  .cover-author-label {{
    font-size: 16.5pt;
    color: #1E293B;
    margin-bottom: 12pt;
  }}
  .cover-badge {{
    border: 2pt solid #4361EE;
    border-radius: 9999px;
    padding: 10pt 42pt;
    background: rgba(255, 255, 255, 0.85);
    display: inline-flex;
    flex-direction: column;
    align-items: center;
  }}
  .author-name {{
    font-size: 20pt;
    font-weight: 700;
    color: #4361EE;
  }}
  .author-contact {{
    font-size: 14.5pt;
    font-weight: 500;
    color: #4361EE;
    margin-top: 2pt;
  }}
</style>
</head>
<body>

  <!-- ==================== SLIDE 1: COVER ==================== -->
  <div class="slide">
    {RINGS_TOP_LEFT}
    {CONTOUR_BOTTOM_RIGHT}
    <div class="content-layer">
      <div class="cover-box">
        <h1 class="cover-title">ANALISIS PERFORMA PRODUK & STRATEGI HARGA TOKOPEDIA</h1>
        <div class="cover-subtitle">STUDI EMPIRIS 28.704 LISTING, ELASTISITAS DISKON & KONSENTRASI WILAYAH</div>
        <div class="cover-author-label">Oleh:</div>
        <div class="cover-badge">
          <div class="author-name">Ferdian Hanif</div>
          <div class="author-contact">ferdianhanif001@gmail.com</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 2: PENDAHULUAN & RUANG LINGKUP DATA ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">PENDAHULUAN & RUANG LINGKUP DATA</h2>
        <div class="slide-subtitle">ANALISIS 28.704 PRODUK TERVALIDASI & 14.128 TOKO DI INDONESIA</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Latar Belakang:</strong> Banyak penjual marketplace terjebak perang harga dan memberikan diskon ekstrem tanpa data yang jelas mengenai titik imbal balik volume dan margin keuntungan bersih.
            </li>
            <li>
              <strong>Ruang Lingkup Data & Metodologi:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Skala Data:</strong> 28.704 listing produk unik dari 14.128 toko di 320+ kota/kabupaten di seluruh Indonesia.</li>
                <li><strong>Pembersihan Data:</strong> Parsing teks regex volume ('rb+ terjual'), deduplikasi URL unik, dan pembersihan listing harga anomali.</li>
                <li><strong>Alur Analitik:</strong> Data mentah ditransformasikan dengan Python dan dimuat ke database relasional SQLite untuk query agregasi.</li>
              </ul>
            </li>
            <li>
              <strong>Tujuan Analisis:</strong> Menemukan batas diskon yang paling optimal dan mengukur tingkat ketergantungan omzet toko di kawasan Jabodetabek.
            </li>
          </ul>
        </div>
        <div class="kpi-container">
          <div class="kpi-grid">
            <div class="kpi-box">
              <div class="kpi-label">Total Listing</div>
              <div class="kpi-val">28.704</div>
              <div class="kpi-desc">Produk bersih tervalidasi</div>
            </div>
            <div class="kpi-box green">
              <div class="kpi-label">Total Penjualan</div>
              <div class="kpi-val">61,7 Juta</div>
              <div class="kpi-desc">Unit barang terdistribusi</div>
            </div>
            <div class="kpi-box amber">
              <div class="kpi-label">Estimasi GMV</div>
              <div class="kpi-val">Rp 16,9 T</div>
              <div class="kpi-desc">Proxy perputaran omzet</div>
            </div>
            <div class="kpi-box purple">
              <div class="kpi-label">Adopsi Diskon</div>
              <div class="kpi-val">34,4%</div>
              <div class="kpi-desc">Listing dengan promosi aktif</div>
            </div>
          </div>
          <div class="kpi-highlight">
            <strong>Konteks Makro:</strong> Toko yang aktif memasang diskon mencakup sepertiga dari total katalog, namun 78% omzet terkonsentrasi pada segmen diskon di bawah 25%.
          </div>
          <div class="chart-card-caption" style="margin-top: 10pt;">Ringkasan Metrik Makro Marketplace Tokopedia (Q1 2026)</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 3: ELASTISITAS DISKON ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">ELASTISITAS DISKON & VOLUME PENJUALAN</h2>
        <div class="slide-subtitle">TITIK OPTIMAL PENJUALAN VS JEBAKAN DISKON DI ATAS 50%</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Masalah Bisnis:</strong> Asumsi bahwa semakin dalam diskon dipotong, volume penjualan pasti akan berlipat ganda.
            </li>
            <li>
              <strong>Temuan Data:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Rentang Optimal (11% - 25%):</strong> Menghasilkan rata-rata 4.552 unit terjual per SKU dengan harga realisasi yang masih sehat (Rp 766.000).</li>
                <li><strong>Diskon Tinggi (26% - 50%):</strong> Penjualan mencapai puncak volume (5.182 unit), namun harga jual rata-rata tertekan ke Rp 405.000.</li>
                <li><strong>Titik Jenuh / Anjlok (> 50%):</strong> Penjualan turun ke 3.767 unit (-27% dari puncak), sementara harga jatuh ke Rp 189.000.</li>
              </ul>
            </li>
            <li>
              <strong>Perilaku Konsumen:</strong> Diskon ekstrem di atas 50% memicu keraguan pembeli atas kualitas barang atau tanggal kedaluwarsa produk.
            </li>
            <li>
              <strong>Rekomendasi Analis:</strong> Terapkan batas diskon maksimal 25%. Alihkan sisa anggaran promosi ke bundling produk (Beli 2 Diskon 15%) atau voucher cashback.
            </li>
          </ul>
        </div>
        <div class="chart-card-single">
          <img src="{FIG1_URI}" alt="Elastisitas Diskon vs Volume">
          <div class="chart-card-caption">Korelasi Kedalaman Diskon vs Rata-Rata Unit Terjual per SKU</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 4: KONSENTRASI WILAYAH ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">KONSENTRASI PASAR & DISPARITAS WILAYAH</h2>
        <div class="slide-subtitle">DOMINASI JABODETABEK & TANTANGAN LOGISTIK LUAR JAWA</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Masalah Bisnis:</strong> Penjual di luar Jabodetabek sering mengeluhkan sepinya pesanan akibat kalah saing ongkos dan durasi pengiriman.
            </li>
            <li>
              <strong>Temuan Data:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Dominasi DKI Jakarta:</strong> Menguasai 82,0% estimasi nilai transaksi nasional dari 44,5% listing produk aktif.</li>
                <li><strong>Kawasan Bodetabek:</strong> Menyumbang 8,4% omzet, sehingga total Jabodetabek mengontrol 90,4% perputaran uang.</li>
                <li><strong>Disparitas Luar Jabodetabek:</strong> Seluruh wilayah di luar Jabodetabek digabung hanya meraih 9,6% perputaran omzet transaksi.</li>
              </ul>
            </li>
            <li>
              <strong>Faktor Kunci Logistik:</strong> Pembeli urban mengutamakan kurir Same-Day / Instant. Lokasi merchant yang jauh membuat ongkos kirim melampaui harga barang.
            </li>
            <li>
              <strong>Rekomendasi Analis:</strong> Penjual luar daerah disarankan menaruh stok di gudang 3PL konsinyasi area Jakarta untuk mengaktifkan kurir instan dan menekan ongkir.
            </li>
          </ul>
        </div>
        <div class="chart-card-single">
          <img src="{FIG2_URI}" alt="Distribusi GMV dan Listing per Wilayah">
          <div class="chart-card-caption">Klaster Jabodetabek Menguasai 90,4% Perputaran Omzet Nasional</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 5: DISTRIBUSI HARGA & PARETO ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">DISTRIBUSI HARGA & ANALISIS PARETO</h2>
        <div class="slide-subtitle">PENGGERAK OMZET UTAMA & KONSENTRASI PADA TOP MERCHANT</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Distribusi Segmen Harga:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Volume Driver:</strong> Produk budget (< Rp 50rb) dan entry (Rp 50rb - 150rb) mencakup 60,1% total katalog produk.</li>
                <li><strong>Revenue Driver:</strong> Produk premium (> Rp 500rb) hanya 19,0% katalog, tetapi menghasilkan 78,7% total perputaran omzet nasional.</li>
              </ul>
            </li>
            <li>
              <strong>Konsentrasi Merchant Ekstrem (Pareto):</strong>
              <ul class="sub-bullet-list">
                <li><strong>Desil 1 (Top 10% Toko):</strong> Menguasai 96,9% perputaran omzet total di platform Tokopedia.</li>
                <li><strong>90% Toko Lainnya:</strong> Berbagi sisa 3,1% omzet pasar, menandakan persaingan sengit pada kelompok penjual long-tail.</li>
              </ul>
            </li>
            <li>
              <strong>Rekomendasi Portofolio:</strong> Terapkan strategi portofolio produk dua lapis: pasang SKU murah untuk mendatangkan ulasan, lalu maksimalkan penjualan SKU bernilai tinggi untuk profitabilitas.
            </li>
          </ul>
        </div>
        <div class="card-stack">
          <div class="chart-card-half">
            <img src="{FIG3_URI}" alt="Distribusi Harga vs GMV">
            <div class="caption">Segmen Premium (> Rp 500rb) Menyumbang 78,7% Estimasi GMV</div>
          </div>
          <div class="chart-card-half">
            <img src="{FIG4_URI}" alt="Konsentrasi Toko Pareto">
            <div class="caption">Kurva Pareto: 10% Toko Teratas Menguasai 96,9% Nilai Transaksi</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 6: STRATEGI & REKOMENDASI (Matching AWS Slide 10) ==================== -->
  <div class="slide">
    {RINGS_TOP_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">RANGKUMAN EKSEKUTIF & AKSI STRATEGIS</h2>
        <div class="slide-subtitle">PANDUAN PRAKTIS PENETAPAN HARGA & EKSPANSI OPERASIONAL</div>
      </div>
      
      <div class="strategy-grid">
        <div class="strategy-card">
          <div class="strategy-card-title pricing">STRATEGI PENETAPAN HARGA & PROMO</div>
          <ul class="strategy-bullets">
            <li><strong>Batas Diskon 25%:</strong> Hentikan diskon > 50% yang terbukti menurunkan volume penjualan sebesar 27% dan merusak margin laba kotor toko.</li>
            <li><strong>Struktur Katalog Bertingkat:</strong> Sediakan produk pembuka (Rp 50rb - 150rb) untuk menjaring ulasan dan algoritma, lalu dorong konversi ke produk margin tinggi.</li>
            <li><strong>Alihkan ke Cashback & Bundling:</strong> Ganti diskon langsung dengan paket Beli 2 Diskon 15% atau cashback koin untuk menaikkan nilai rata-rata keranjang (AOV).</li>
            <li><strong>Pertahankan Reputasi:</strong> Jaga rating toko di atas 4,8 bintang; toko bereputasi Official / Power Merchant mencatat konversi 2,4x lebih tinggi.</li>
          </ul>
        </div>
        
        <div class="strategy-card">
          <div class="strategy-card-title logistics">STRATEGI LOGISTIK & DISTRIBUSI</div>
          <ul class="strategy-bullets">
            <li><strong>Hub Fulfillment Jabodetabek:</strong> Manfaatkan gudang konsinyasi 3PL di Jakarta untuk melayani 90,4% pasar nasional dengan ongkir terendah.</li>
            <li><strong>Aktivasi Pengiriman Cepat:</strong> Aktifkan kurir Same-Day & Instant; kecepatan pengiriman menjadi penentu utama konversi checkout pembeli kota besar.</li>
            <li><strong>Fokus Produk Nilai Tinggi:</strong> Hindari perang harga pada komoditas murah; arahkan inventori pada produk di atas Rp 200rb yang menyumbang mayoritas omzet.</li>
            <li><strong>Diversifikasi Produk Unggulan:</strong> Hindari ketergantungan pada 1 produk andalan guna memitigasi risiko jika terjadi perubahan tren atau algoritma pencarian.</li>
          </ul>
        </div>
      </div>

      <div class="diagnostic-terminal">
        <div class="term-title">Rencana Implementasi & Evaluasi Bertahap:</div>
        <div class="term-line">
          • <span class="term-highlight">Bulan 1 (Optimasi Harga):</span> Audit seluruh katalog, tetapkan batas atas diskon 25%, dan ganti promo potongan harga ekstrem dengan sistem voucher bundling.
        </div>
        <div class="term-line">
          • <span class="term-highlight">Bulan 2 (Ekspansi Logistik):</span> Uji coba penempatan stok 20% SKU terlaris pada fasilitas gudang 3PL Jakarta untuk mengaktifkan opsi pengiriman Same-Day.
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

def save_html_template():
    with open(HTML_TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"HTML template written: {HTML_TEMPLATE_PATH}")

async def render_pdf():
    save_html_template()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Viewport with exact aspect ratio 1080pt x 607.92pt (1440px x 811px)
        page = await browser.new_page(viewport={"width": 1440, "height": 811})
        file_url = f"file:///{HTML_TEMPLATE_PATH.replace(os.sep, '/')}"
        print(f"Loading slide deck: {file_url}")
        await page.goto(file_url, wait_until="networkidle")
        # Ensure web fonts are completely loaded
        await page.evaluate("document.fonts.ready")
        await asyncio.sleep(1.0)
        
        await page.pdf(
            path=PDF_OUTPUT_PATH,
            prefer_css_page_size=True,
            print_background=True,
            page_ranges="1-6",
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        await browser.close()
        print(f"Executive Presentation Deck successfully generated: {PDF_OUTPUT_PATH}")
        
    # Clean up temporary HTML file so repository only retains presentation_deck.pdf
    if os.path.exists(HTML_TEMPLATE_PATH):
        os.remove(HTML_TEMPLATE_PATH)
        print("Cleaned up temporary HTML template.")

if __name__ == "__main__":
    asyncio.run(render_pdf())

