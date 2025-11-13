import streamlit as st
import pandas as pd

st.title("Data Dashboard - Summary & Charts")
st.write("Menampilkan ringkasan total dan rata-rata data penjualan.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv", parse_dates=["Date"])
    return df

df = load_data()

# Bagian 1 Table Data
st.write("Data Penjualan")
st.dataframe(df)

# Bagian 2: Summary Statistik
st.write("Ringkasan Data (Summary)")

total_sales = df["Sales"].sum()
avg_sales = df["Sales"].mean()
max_sales = df["Sales"].max()
min_sales = df["Sales"].min()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Rata-rata Sales", f"${avg_sales:,.0f}")
col3.metric("Penjualan Tertinggi", f"${max_sales:,.0f}")
col4.metric("Penjualan Terendah", f"${min_sales:,.0f}")

# Bagian 3: Visualisasi Berdasarkan Kategori
st.write("Penjualan per Kategori")
sales_by_cat = df.groupby("Category")["Sales"].sum()
st.bar_chart(sales_by_cat)

# Bagian 4: Tren Penjualan Harian
st.write("Tren Penjualan Harian")
sales_by_date = df.groupby("Date")["Sales"].sum()
st.line_chart(sales_by_date)

# Bagian 5: Insight Otomatis
st.write("Insight Otomatis")
top_product = df.loc[df["Sales"].idxmax(), "Product"]
st.info(f"Produk dengan penjualan tertinggi adalah **{top_product}** dengan nilai **${max_sales:,.0f}**.")