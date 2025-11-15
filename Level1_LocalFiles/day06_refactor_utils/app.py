import streamlit as st
from utils import smart_load_csv, calculate_summary

st.title("Smart Data Dashboard")

df, sales_col = smart_load_csv("data/sales.csv")
st.subheader("Data Loaded")
st.write(df)

summary = calculate_summary(df, sales_col)

st.subheader("Summary")

if sales_col:
    st.metric("Total", summary["total"])
    st.metric("Average", summary["average"])
    st.metric("Max", summary["max"])
else:
    st.warning("Tidak ada kolom angka untuk summary. Tampilkan data saja.")
