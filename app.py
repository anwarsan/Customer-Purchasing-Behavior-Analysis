import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Interactive RFM Dashboard", layout="wide")

st.title("🚀 Interactive E-Commerce RFM Dashboard")
st.markdown("Dashboard ini memungkinkan kita untuk mengeksplorasi segmen pelanggan secara interaktif.")

# Load Data
@st.cache_data
def load_data():
    # Pastikan file CSV berada di folder yang sama
    df = pd.read_csv('RFM.csv')
    return df

df_rfm = load_data()

# --- SIDEBAR FILTER ---
st.sidebar.header("User Filter")
segments = st.sidebar.multiselect(
    "Pilih Segmen Pelanggan:",
    options=df_rfm["customers_segment"].unique(),
    default=df_rfm["customers_segment"].unique()
)

# Filter Dataframe berdasarkan input sidebar
df_selection = df_rfm[df_rfm["customers_segment"].isin(segments)]

# --- MAIN PAGE: KPI ---
total_cust = len(df_selection)
avg_monetary = df_selection['Monetary'].mean()
avg_freq = df_selection['Frequency'].mean()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pelanggan", f"{total_cust:,}")
with col2:
    st.metric("Rata-rata Transaksi (Monetary)", f"{avg_monetary:.2f}")
with col3:
    st.metric("Rata-rata Frekuensi", f"{avg_freq:.2f}")

st.divider()

# --- VISUALISASI PLOTLY ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Distribusi Segmen (Bar Chart)")
    # Menghitung jumlah per segmen
    segment_counts = df_selection['customers_segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    fig_bar = px.bar(
        segment_counts, 
        x='Count', 
        y='Segment', 
        orientation='h',
        color='Segment',
        title="Jumlah Customer per Segmen",
        template="plotly_white"
    )
    # --- BAGIAN PENTING: Menghapus Legend ---
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with row1_col2:
    st.subheader("Recency vs Frequency Analysis")
    fig_scatter = px.scatter(
        df_selection,
        x="Recency",
        y="Frequency",
        color="customers_segment",
        size="Monetary",
        hover_name="user_id",
        log_y=True, # Menggunakan skala log jika data frequency sangat kontras
        title="Hubungan Recency, Frequency, & Monetary",
        template="plotly_dark"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- TABEL DATA ---
with st.expander("Lihat Detail Data Mentah"):
    st.dataframe(df_selection)

st.divider()
st.header("📌 Analisis Strategis")

# Menggunakan expander agar dashboard tetap ringkas
with st.expander("Klik untuk melihat Insight & Rekomendasi Strategis", expanded=True):
    col_ins, col_rec = st.columns(2)
    
    with col_ins:
        st.markdown("### 💡 Insight Utama")
        st.write("""
        * **Dominasi Big Spenders:** Segmen ini memiliki populasi besar, menunjukkan bahwa platform berhasil menarik pengguna dengan daya beli tinggi.
        * **Retensi Loyalitas:** Sekitar 45% pelanggan adalah *repeat buyers*. Ini adalah aset berharga yang perlu dijaga agar tidak berpindah ke kompetitor.
        * **Kesenjangan Konversi:** Meskipun traffic tinggi, CVR rata-rata masih di angka 0.9%, menunjukkan adanya hambatan (*friction*) saat proses checkout.
        """)

    with col_rec:
        st.markdown("### 🎯 Rekomendasi & Fokus Strategis")
        st.write("""
        * **Program Loyalitas (Tiered):** Fokuskan pada segmen *Best Customers* dengan akses eksklusif atau sistem poin untuk meningkatkan *switching cost*.
        * **Win-back Campaign:** Segmen *Almost Lost* harus diprioritaskan dengan promo berbasis urgensi (diskon dengan batas waktu) untuk memicu transaksi kembali.
        * **Optimasi Checkout:** Perbaiki pengalaman halaman pembayaran dan tawarkan voucher gratis ongkir, yang terbukti menjadi faktor penentu utama transaksi.
        """)
