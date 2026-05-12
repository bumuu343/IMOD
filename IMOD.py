import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="IMOD Database", page_icon="🪨", layout="wide")

st.title("🪨 Industrial Mineral Open-Database (IMOD)")
st.write("Sistem pangkalan data pengurusan maklumat mineral perindustrian.")

# 2. Persediaan Data (Menggunakan data rasmi jurnal)
@st.cache_data
def load_data():
    data = {
        "ID": ["001", "002", "003"],
        "Mineral Name": ["Limestone (Calcite)", "Kaolin (Kaolinite)", "Silica Sand (Quartz)"],
        "Category": ["Carbonates", "Phyllosilicates (Clays)", "Tectosilicates (Silicates)"],
        "Hardness (Mohs)": [3.0, 2.0, 7.0],
        "Chemical Formula": ["CaCO3", "Al2Si2O5(OH)4", "SiO2"],
        "Primary Application": [
            "Cement manufacturing, steel smelting flux, agriculture",
            "Pharmaceutical excipients, cosmetics, paper coating",
            "Refractory materials, silicon metal ore, glassmaking"
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Antaramuka Carian (Search & Filter)
st.subheader("🔍 Carian Pangkalan Data")
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input("Cari mineral atau aplikasi (cth: Glassmaking, Cement, Kaolin):")
with col2:
    kategori_filter = st.selectbox("Tapis ikut Kategori:", ["Semua", "Carbonates", "Phyllosilicates (Clays)", "Tectosilicates (Silicates)"])

# 4. Logik Sistem Carian
if kategori_filter != "Semua":
    df = df[df["Category"] == kategori_filter]

if search_query:
    # Cari dalam semua lajur Teks
    df = df[
        df["Mineral Name"].str.contains(search_query, case=False, na=False) |
        df["Primary Application"].str.contains(search_query, case=False, na=False) |
        df["Chemical Formula"].str.contains(search_query, case=False, na=False)
    ]

# 5. Paparan Jadual (Data Retrieval)
st.write(f"Menjumpai **{len(df)}** rekod:")
st.dataframe(df, use_container_width=True, hide_index=True)

# 6. Profil Terperinci (Detailed View)
st.divider()
st.subheader("📄 Profil Terperinci Mineral")
pilihan_mineral = st.selectbox("Pilih mineral untuk lihat profil penuh:", df["Mineral Name"].tolist())

if pilihan_mineral:
    # Tarik data spesifik baris tersebut
    profil = df[df["Mineral Name"] == pilihan_mineral].iloc[0]
    
    colA, colB = st.columns(2)
    with colA:
        st.write(f"**Kategori:** {profil['Category']}")
        st.write(f"**Formula Kimia:** {profil['Chemical Formula']}")
    with colB:
        st.write(f"**Skala Mohs:** {profil['Hardness (Mohs)']}")
        st.write(f"**Aplikasi:** {profil['Primary Application']}")
