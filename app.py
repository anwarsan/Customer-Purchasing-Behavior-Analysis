import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce RFM Dashboard", layout="wide")

st.title("📊 E-Commerce RFM Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('RFM.csv')
    return df

df_rfm = load_data()

# Sidebar Filter
st.sidebar.header("Filter")
segment = st.sidebar.multiselect("Pilih Segmen:", 
                                options=df_rfm["customers_segment"].unique(),
                                default=df_rfm["customers_segment"].unique())

df_selection = df_rfm[df_rfm["customers_segment"].isin(segment)]

# KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{len(df_selection):,}")
col2.metric("Avg Frequency", f"{df_selection['Frequency'].mean():.2f}")
col3.metric("Total Monetary", f"{df_selection['Monetary'].sum():.2f}")

# Visualisasi
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Distribusi Segmen Pelanggan")
    fig, ax = plt.subplots()
    sns.countplot(data=df_selection, y='customers_segment', ax=ax, palette='viridis')
    st.pyplot(fig)

with right_column:
    st.subheader("Recency vs Frequency")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_selection, x='Recency', y='Frequency', hue='customers_segment', ax=ax)
    st.pyplot(fig)
