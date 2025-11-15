import pandas as pd

def smart_load_csv(path="data/sales.csv"):
    # Load CSV tanpa asumsi khusus
    df = pd.read_csv(path)

    # --- SMART DETECTION ---

    # 1. Deteksi kolom tanggal
    date_candidates = ["date", "tanggal", "day", "time"]
    for col in df.columns:
        if col.lower() in date_candidates:
            df[col] = pd.to_datetime(df[col], errors="ignore")
            df.rename(columns={col: "Date"}, inplace=True)
            break  # ambil 1 saja

    # 2. Deteksi kolom angka penjualan
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # Kemungkinan nama kolom sales
    possible_sales = ["sales", "amount", "total", "revenue", "price"]

    sales_col = None
    for col in df.columns:
        if col.lower() in possible_sales:
            sales_col = col
            break

    # Jika tidak ditemukan, tapi ada kolom numerik → ambil pertama
    if sales_col is None and len(numeric_cols) > 0:
        sales_col = numeric_cols[0]

    # Return df + kolom sales yang ditemukan
    return df, sales_col


def calculate_summary(df, sales_col):
    if sales_col is None:
        return {
            "total": None,
            "average": None,
            "max": None
        }

    return {
        "total": df[sales_col].sum(),
        "average": df[sales_col].mean(),
        "max": df[sales_col].max(),
    }
