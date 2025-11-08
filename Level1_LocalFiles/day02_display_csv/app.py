import streamlit as st
import pandas as pd

st.title(" Data Dashboard - Display CSV")

st.write("### Upload atau gunakan sample CSV")

# Opsi upload file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File berhasil diupload")
else:
    # Default data (local)
    df = pd.read_csv("data/sample_data.csv")
    st.info("Menampilkan sample_data.csv bawaan")

# Ringkasan sederhana
st.write("### Statistik Ringkas")
st.write(df.describe())

# Visualisasi ringan
st.write("### Total Penjualan per Kategori")
sales_by_cat = df.groupby("Category")["Sales"].sum()
st.bar_chart(sales_by_cat)
