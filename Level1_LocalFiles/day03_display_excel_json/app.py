import streamlit as st
import pandas as pd

st.title("📂 Data Dashboard — Excel & JSON Viewer")

st.sidebar.header("📁 Pilih Jenis File")
file_type = st.sidebar.selectbox("Pilih format data:", ["Excel", "JSON"])

if file_type == "Excel":
    st.subheader("📘 Menampilkan Data dari Excel")
    uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.success("File Excel berhasil diupload!")
    else:
        df = pd.read_excel("data/sales_data.xlsx")
        st.info("Menampilkan sample sales_data.xlsx bawaan")

elif file_type == "JSON":
    st.subheader("🧩 Menampilkan Data dari JSON")
    uploaded_file = st.file_uploader("Upload file JSON", type=["json"])
    
    if uploaded_file is not None:
        df = pd.read_json(uploaded_file)
        st.success("File JSON berhasil diupload!")
    else:
        df = pd.read_json("data/products.json")
        st.info("Menampilkan sample products.json bawaan")

# Tampilkan DataFrame
st.write("### 📋 Data Preview")
st.dataframe(df)

# Statistik Ringkas (hanya untuk numeric)
st.write("### 📈 Statistik Data")
st.write(df.describe())

# Visualisasi (jika ada kolom numerik)
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
if len(numeric_cols) >= 1:
    st.write("### 📊 Visualisasi Ringkas")
    st.bar_chart(df[numeric_cols])
else:
    st.warning("Tidak ada kolom numerik untuk divisualisasikan.")
