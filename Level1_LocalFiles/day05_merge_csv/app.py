import streamlit as st
import pandas as pd

st.title("Mini Project — Merge CSV (Sales + Products)")
st.write("Menggabungkan data penjualan dengan daftar produk.")

@st.cache_data
def load_data():
    sales_raw = pd.read_csv("data/sales.csv")

    st.subheader("🔍 Debug Info")
    st.write("Kolom dalam sales.csv:")
    st.write(list(sales_raw.columns))

    # Cari kolom tanggal otomatis
    possible_date_cols = ["Date", "date", "Tanggal", "tanggal"]
    date_col = next((c for c in possible_date_cols if c in sales_raw.columns), None)

    if date_col:
        sales = pd.read_csv("data/sales.csv", parse_dates=[date_col])
        st.success(f"Kolom tanggal terdeteksi: {date_col}")
    else:
        sales = sales_raw.copy()
        st.warning("⚠ Tidak ada kolom tanggal.")

    # Baca produk
    products = pd.read_csv("data/products.csv")

    # Merge
    df = pd.merge(sales, products, on="ProductID", how="left")

    # Hitung TotalSales jika kolom tersedia
    if "Quantity" in df.columns and "Price" in df.columns:
        df["TotalSales"] = df["Quantity"] * df["Price"]

    return df


df = load_data()
st.subheader("📄 Data Gabungan")
st.dataframe(df)

st.subheader("📊 Statistik")
col1, col2, col3 = st.columns(3)

# Jumlah transaksi
col1.metric("Total Transaksi", len(df))

# Quantity aman
if "Quantity" in df.columns:
    col2.metric("Total Quantity", int(df["Quantity"].sum()))
else:
    col2.metric("Total Quantity", "N/A")

# TotalSales aman
if "TotalSales" in df.columns:
    col3.metric("Total Sales", f"${df['TotalSales'].sum():,.0f}")
else:
    col3.metric("Total Sales", "N/A")
