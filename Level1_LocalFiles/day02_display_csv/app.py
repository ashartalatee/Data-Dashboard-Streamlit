import streamlit as st
import pandas as pd
import io

# 🧠 SMART CSV LOADER (Universal + Clean)
def load_csv_safely(file):
    """Membaca CSV apapun dengan aman, auto-handle encoding, kutipan rusak, dan pembersihan kolom."""
    try:
        # 1️⃣ Coba baca normal (UTF-8)
        df = pd.read_csv(file, sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')

    except UnicodeDecodeError:
        # 2️⃣ Coba fallback ke latin1
        file.seek(0)
        df = pd.read_csv(file, sep=None, engine='python', encoding='latin1', on_bad_lines='skip')

    except pd.errors.ParserError:
        # 3️⃣ Tangani CSV rusak (kutipan tidak seimbang)
        file.seek(0)
        content = file.read()
        if isinstance(content, bytes):
            content = content.decode('latin1', errors='ignore')

        clean_content = content.replace('"', '')  # hapus kutipan aneh
        df = pd.read_csv(io.StringIO(clean_content), sep=None, engine='python', on_bad_lines='skip')

    # 4️⃣ Bersihkan dan rapikan DataFrame
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df = df.dropna(how='all')
    return df


# 🎨 STREAMLIT DASHBOARD UI
st.set_page_config(page_title="Smart CSV Dashboard v2", layout="wide")

st.title("📊 Smart CSV Dashboard v2 — Universal + Clean Edition")

st.markdown("""
Unggah file CSV **apa pun**, dashboard ini akan otomatis:
- ✅ Membaca file dengan aman (auto encoding & delimiter)
- 🧠 Membersihkan nama kolom & baris kosong
- 📊 Menampilkan ringkasan data dan statistik
- 📈 Membuat grafik otomatis untuk kolom numerik
""")

uploaded_file = st.file_uploader("📂 Upload file CSV Anda", type="csv")


# 🚀 MAIN LOGIC
if uploaded_file is not None:
    try:
        df = load_csv_safely(uploaded_file)
    except Exception as e:
        st.error(f"❌ Gagal membaca file CSV: {e}")
        df = None

    if df is not None and not df.empty:
        st.success(f"✅ Data berhasil dimuat! ({len(df)} baris × {len(df.columns)} kolom)")

        # --- PREVIEW ---
        st.subheader("👀 Preview Data (10 baris pertama)")
        st.dataframe(df.head(10), use_container_width=True)

        # --- INFORMASI DASAR ---
        st.subheader("🧩 Informasi Struktur Data")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        # --- DESKRIPSI STATISTIK ---
        st.subheader("📈 Statistik Ringkasan")
        st.write(df.describe(include='all').transpose())

        # --- VISUALISASI ---
        st.subheader("📊 Visualisasi Kolom Numerik")
        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if numeric_cols:
            selected_col = st.selectbox("Pilih kolom untuk visualisasi:", numeric_cols)
            st.bar_chart(df[selected_col])
        else:
            st.info("📌 Tidak ada kolom numerik untuk divisualisasikan.")

    else:
        st.warning("⚠️ File kosong atau tidak bisa dibaca dengan benar.")
else:
    st.info("⬆️ Silakan upload file CSV untuk mulai analisis.")


# 🧾 FOOTER
st.markdown("""
---
### ✅ Tips Agar Dashboard Berjalan Optimal
- Gunakan file **< 100 MB**
- Pastikan **ada header kolom**
- Hindari campuran tanda pemisah (`,` dan `;` bersamaan)
- Simpan file dengan **encoding UTF-8** bila memungkinkan  

💡 *Dibuat oleh **Ashar** — Python Automation for Data & Business (end-to-end)*  
📘 Level 1 · Day 2 · Project: **Universal CSV Dashboard**
""")
