import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler

# ===================================================================
# 1. PAGE CONFIGURATION
# ===================================================================
st.set_page_config(
    page_title="Retail Customer Segmentation Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ===================================================================
# 2. CSS STYLING (DARK MODE SUPPORT)
# ===================================================================
st.markdown("""
<style>
    /* Metric Card Style */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    /* Highlight Table Header */
    thead tr th:first-child {display:none}
    tbody th {display:none}
</style>
""", unsafe_allow_html=True)

st.title("🛍️ Retail Customer Segmentation Dashboard")
st.markdown("Analisis perilaku pelanggan: **RFM Analysis** + **K-Means Clustering** + **Customer Profiling**.")

# ===================================================================
# 3. LOAD DATA FUNCTIONS
# ===================================================================
@st.cache_data
def load_data(file):
    try:
        return pd.read_csv(file, encoding="utf-8")
    except:
        try:
            return pd.read_csv(file, encoding="latin1")
        except:
            return pd.read_csv(file, encoding="ISO-8859-1")

# ===================================================================
# 4. SIDEBAR SETUP
# ===================================================================
st.sidebar.header("📂 Data Configuration")
uploaded_file = st.sidebar.file_uploader("Upload RFM Result (CSV)", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("✅ File loaded successfully!")

    # --- COLUMN MAPPING ---
    st.sidebar.subheader("🔧 Map Columns")
    all_cols = df.columns.tolist()
    
    # Helper index finder
    def get_index(keyword, columns):
        matches = [i for i, col in enumerate(columns) if keyword.lower() in col.lower()]
        return matches[0] if matches else 0

    col_id = st.sidebar.selectbox("Customer ID Column", all_cols, index=get_index("id", all_cols))
    col_cluster = st.sidebar.selectbox("Cluster Column", all_cols, index=get_index("luster", all_cols))
    col_recency = st.sidebar.selectbox("Recency Column", all_cols, index=get_index("ecency", all_cols))
    col_frequency = st.sidebar.selectbox("Frequency Column", all_cols, index=get_index("requency", all_cols))
    col_monetary = st.sidebar.selectbox("Monetary Column", all_cols, index=get_index("onetary", all_cols))

    # ===================================================================
    # 🔥 DATA CLEANING & TYPE CONVERSION (FIX ERROR DI SINI)
    # ===================================================================
    # 1. Konversi paksa kolom RFM ke Numerik. Jika gagal (teks/error), jadi NaN.
    df[col_recency] = pd.to_numeric(df[col_recency], errors='coerce')
    df[col_frequency] = pd.to_numeric(df[col_frequency], errors='coerce')
    df[col_monetary] = pd.to_numeric(df[col_monetary], errors='coerce')
    
    # 2. Hapus baris yang mengandung NaN di kolom penting (agar tidak error saat plotting/ranking)
    rows_before = len(df)
    df.dropna(subset=[col_recency, col_frequency, col_monetary], inplace=True)
    rows_after = len(df)
    
    if rows_before != rows_after:
        st.sidebar.warning(f"⚠️ {rows_before - rows_after} baris data dihapus karena format angka tidak valid.")

    # 3. Convert ID & Cluster to string for better visualization
    df[col_cluster] = df[col_cluster].astype(str)
    df[col_id] = df[col_id].astype(str)
    
    clusters = sorted(df[col_cluster].unique())

    # ===================================================================
    # 5. MAIN DASHBOARD TABS
    # ===================================================================
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Executive Summary", 
        "🏆 Top Customer & Lookup", 
        "🧩 Cluster Profiling", 
        "🐍 Snake Plot",
        "🔍 3D & PCA View", 
        "📥 Data Export"
    ])

    # -------------------------------------------------------------------
    # TAB 1: EXECUTIVE SUMMARY
    # -------------------------------------------------------------------
    with tab1:
        st.header("Global Business Overview")
        
        total_customers = len(df)
        total_sales = df[col_monetary].sum()
        avg_sales = df[col_monetary].mean()
        avg_freq = df[col_frequency].mean()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Customers", f"{total_customers:,}")
        c2.metric("Total Revenue", f"${total_sales:,.2f}")
        c3.metric("Avg Spend/Cust", f"${avg_sales:,.2f}")
        c4.metric("Avg Frequency", f"{avg_freq:.2f}x")

        st.divider()

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Customer Distribution")
            fig_pie = px.pie(df, names=col_cluster, title="Proportion of Customers per Cluster",
                             color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_b:
            st.subheader("Revenue Contribution")
            rev_per_cluster = df.groupby(col_cluster)[col_monetary].sum().reset_index()
            fig_bar = px.bar(rev_per_cluster, x=col_cluster, y=col_monetary, color=col_cluster,
                             title="Total Revenue by Cluster", text_auto='.2s')
            st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------------------------------------------------
    # TAB 2: TOP CUSTOMER & LOOKUP
    # -------------------------------------------------------------------
    with tab2:
        st.header("🏆 Top Customers Rankings")
        st.caption("Siapa pelanggan terbaik Anda? Berikut adalah Top 10 berdasarkan kategori.")

        # Top 10 Tables
        row1_1, row1_2, row1_3 = st.columns(3)

        with row1_1:
            st.markdown("#### 💰 Top Spenders (Monetary)")
            top_monetary = df.nlargest(10, col_monetary)[[col_id, col_monetary, col_cluster]]
            st.dataframe(top_monetary.style.format({col_monetary: "${:,.2f}"}), hide_index=True, use_container_width=True)

        with row1_2:
            st.markdown("#### 🔄 Most Frequent (Frequency)")
            top_freq = df.nlargest(10, col_frequency)[[col_id, col_frequency, col_cluster]]
            st.dataframe(top_freq, hide_index=True, use_container_width=True)
        
        with row1_3:
            st.markdown("#### ⚡ Most Recent (Recency)")
            # Recency terkecil = Terbaik (baru belanja)
            # Karena sudah dikonversi ke numerik di atas, nsmallest ini aman sekarang.
            top_rec = df.nsmallest(10, col_recency)[[col_id, col_recency, col_cluster]]
            st.dataframe(top_rec, hide_index=True, use_container_width=True)

        st.divider()

        # --- CUSTOMER LOOKUP SECTION ---
        st.header("🕵️ Customer Analysis (Lookup)")
        st.caption("Cari ID Pelanggan untuk melihat detail profil mereka.")

        # Search Box
        search_id = st.selectbox("Pilih / Ketik Customer ID:", options=df[col_id].unique())

        if search_id:
            # Filter Data
            cust_data = df[df[col_id] == search_id].iloc[0]
            
            # Tampilkan Card Detail
            st.markdown(f"### 👤 Profile: {search_id}")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Cluster Group", cust_data[col_cluster])
            m2.metric("Total Belanja (Monetary)", f"${cust_data[col_monetary]:,.2f}")
            m3.metric("Total Transaksi (Frequency)", f"{int(cust_data[col_frequency])}x")
            m4.metric("Terakhir Belanja (Recency)", f"{int(cust_data[col_recency])} hari lalu")

            # Insight Tambahan
            if cust_data[col_recency] > df[col_recency].quantile(0.75):
                st.warning("⚠️ Pelanggan ini sudah lama tidak berbelanja (Churn Risk).")
            elif cust_data[col_monetary] > df[col_monetary].quantile(0.90):
                st.success("💎 Ini adalah pelanggan VIP (Top 10% Spender).")
            else:
                st.info("ℹ️ Pelanggan aktif standar.")

    # -------------------------------------------------------------------
    # TAB 3: CLUSTER PROFILING
    # -------------------------------------------------------------------
    with tab3:
        st.header("Cluster Profiling")
        
        summary_df = df.groupby(col_cluster)[[col_recency, col_frequency, col_monetary]].agg(['mean', 'median', 'count'])
        st.dataframe(summary_df.style.highlight_max(axis=0, color='darkgreen'), use_container_width=True)

        st.subheader("Distribution Boxplots")
        b1, b2, b3 = st.columns(3)
        b1.plotly_chart(px.box(df, x=col_cluster, y=col_recency, color=col_cluster, title="Recency"), use_container_width=True)
        b2.plotly_chart(px.box(df, x=col_cluster, y=col_frequency, color=col_cluster, title="Frequency"), use_container_width=True)
        b3.plotly_chart(px.box(df, x=col_cluster, y=col_monetary, color=col_cluster, title="Monetary"), use_container_width=True)

    # -------------------------------------------------------------------
    # TAB 4: SNAKE PLOT
    # -------------------------------------------------------------------
    with tab4:
        st.header("🐍 Snake Plot (Behavior Analysis)")
        
        scaler = StandardScaler()
        df_norm = df[[col_recency, col_frequency, col_monetary]].copy()
        df_norm = pd.DataFrame(scaler.fit_transform(df_norm), columns=['Recency', 'Frequency', 'Monetary'])
        df_norm['Cluster'] = df[col_cluster].values # Use .values to ensure alignment
        
        df_melt = pd.melt(df_norm.reset_index(), id_vars=['Cluster'], 
                          value_vars=['Recency', 'Frequency', 'Monetary'], 
                          var_name='Attribute', value_name='Standardized Value')
        
        snake_plot = px.line(df_melt.groupby(['Cluster', 'Attribute'])['Standardized Value'].mean().reset_index(), 
                             x="Attribute", y="Standardized Value", color='Cluster', line_group='Cluster', markers=True)
        st.plotly_chart(snake_plot, use_container_width=True)

    # -------------------------------------------------------------------
    # TAB 5: ADVANCED VISUALIZATION
    # -------------------------------------------------------------------
    with tab5:
        st.header("3D & PCA View")
        viz_choice = st.radio("Select View:", ["3D RFM", "2D PCA"], horizontal=True)

        if viz_choice == "3D RFM":
            fig_3d = px.scatter_3d(df, x=col_recency, y=col_frequency, z=col_monetary, color=col_cluster, opacity=0.7, height=600)
            st.plotly_chart(fig_3d, use_container_width=True)
        else:
            pca_cols = [c for c in df.columns if "PCA" in c or "pca" in c] # Case insensitive check
            if len(pca_cols) >= 2:
                fig_pca = px.scatter(df, x=pca_cols[0], y=pca_cols[1], color=col_cluster, height=500)
                st.plotly_chart(fig_pca, use_container_width=True)
            else:
                st.warning("⚠️ Kolom PCA (misal PCA1, PCA2) tidak ditemukan di file CSV ini.")

    # -------------------------------------------------------------------
    # TAB 6: EXPORT
    # -------------------------------------------------------------------
    with tab6:
        st.header("Data Export")
        
        sel_cluster = st.multiselect("Filter Cluster", options=clusters, default=clusters)
        filtered_df = df[df[col_cluster].isin(sel_cluster)]
        st.dataframe(filtered_df)
        
        st.download_button("Download CSV", filtered_df.to_csv(index=False).encode('utf-8'), "rfm_filtered.csv", "text/csv")

else:
    st.info("👋 Silakan upload file CSV di sidebar untuk memulai.")