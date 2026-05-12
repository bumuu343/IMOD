import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="IMOD Database", page_icon="🪨", layout="wide")

st.title("🪨 Industrial Mineral Open-Database (IMOD)")
st.write("Sistem pangkalan data pengurusan maklumat mineral perindustrian.")

# 2. Persediaan Data (Mock Database)
@st.cache_data
def load_data():
    data = {
        "ID": ["001", "002", "003"],
        "Nama Mineral": ["Batu Kapur (Limestone)", "Kaolin", "Pasir Silika (Quartz)"],
        "Kategori": ["Karbonat", "Tanah Liat", "Silikat"],
        "Kekerasan (Mohs)": [3.0, 2.0, 7.0],
        "Formula Kimia": ["CaCO3", "Al2Si2O5(OH)4", "SiO2"],
        "Aplikasi Utama": [
            "Pembuatan Simen, Agen Fluks, Pertanian",
            "Salutan Kertas, Seramik, Farmaseutikal",
            "Pembuatan Kaca, Pasir Foundri, Fracking"
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Antaramuka Carian (Search & Filter)
st.subheader("🔍 Carian Pangkalan Data")
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input("Cari mineral atau aplikasi (cth: Kaca, Simen, Kaolin):")
with col2:
    kategori_filter = st.selectbox("Tapis ikut Kategori:", ["Semua", "Karbonat", "Tanah Liat", "Silikat"])

# 4. Logik Sistem Carian
if kategori_filter != "Semua":
    df = df[df["Kategori"] == kategori_filter]

if search_query:
    # Cari dalam semua lajur Teks
    df = df[
        df["Nama Mineral"].str.contains(search_query, case=False, na=False) |
        df["Aplikasi Utama"].str.contains(search_query, case=False, na=False) |
        df["Formula Kimia"].str.contains(search_query, case=False, na=False)
    ]

# 5. Paparan Jadual (Data Retrieval)
st.write(f"Menjumpai **{len(df)}** rekod:")
st.dataframe(df, use_container_width=True, hide_index=True)

# 6. Profil Terperinci (Detailed View)
st.divider()
st.subheader("📄 Profil Terperinci Mineral")
pilihan_mineral = st.selectbox("Pilih mineral untuk lihat profil penuh:", df["Nama Mineral"].tolist())

if pilihan_mineral:
    # Tarik data spesifik baris tersebut
    profil = df[df["Nama Mineral"] == pilihan_mineral].iloc[0]
    
    colA, colB = st.columns(2)
    with colA:
        st.write(f"**Kategori:** {profil['Kategori']}")
        st.write(f"**Formula Kimia:** {profil['Formula Kimia']}")
    with colB:
        st.write(f"**Skala Mohs:** {profil['Kekerasan (Mohs)']}")
        st.write(f"**Aplikasi:** {profil['Aplikasi Utama']}")