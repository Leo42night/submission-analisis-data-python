import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np

# Load dataset
@st.cache_data
def load_data():    
    df = pd.read_csv("dashboard/main_data.csv") # path relative terhadap tempat streamlit dijalankan
    return df

df = load_data()

# Judul Dashboard
st.title("📊 Bike Sharing Dashboard")

# Sidebar untuk navigasi
tab = st.sidebar.radio("Pilih Pertanyaan", [
    "Bagaimana pengaruh suhu (temp) dan kelembaban (hum) terhadap jumlah pengguna sepeda (cnt)?",
    "Apa perbedaan jumlah pengguna sepeda antara pengguna casual dan pengguna registered pada hari libur dan hari kerja?",
    "Bagaimana Pola Penggunaan Sepeda dalam Sehari, terutama berdasarkan pengaruh cuaca?"
])

# **1. Diagram Clustering Manual Grouping (Binning) Suhu vs Jumlah Pengguna**
if tab == "Bagaimana pengaruh suhu (temp) dan kelembaban (hum) terhadap jumlah pengguna sepeda (cnt)?":
    # Definisikan rentang suhu dalam derajat Celsius
    temp_bins = [0, 8.2, 16.4, 24.6, 32.8, 41]  # Skala 0-1 dikali 41
    temp_labels = ['Sangat Dingin (0-8°C)', 'Dingin (8-16°C)', 'Normal (16-24°C)', 'Hangat (24-32°C)', 'Panas (32-41°C)']
    df['temp_group'] = pd.cut(df['temp'] * 41, bins=temp_bins, labels=temp_labels)  # Pastikan temp dikonversi ke °C

    # Visualisasi rata-rata jumlah pengguna berdasarkan suhu
    st.subheader("📊 Jumlah Pengguna Sepeda Berdasarkan Kelompok Suhu")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='temp_group', y=df['cnt'] / 1_000_000, data=df, estimator=sum, hue='temp_group', palette='coolwarm', ax=ax)
    ax.set_xlabel('Kelompok Suhu')
    ax.set_ylabel('Jumlah Pengguna Sepeda (Juta)')
    ax.set_title('Pengaruh Suhu terhadap Penggunaan Sepeda')
    st.pyplot(fig)

    # -----------------------------------------------

    # Manual Grouping atau Binning untuk kelembaban
    hum_bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    hum_labels = ['Sangat Kering', 'Kering', 'Normal', 'Lembab', 'Sangat Lembab']
    df['hum_group'] = pd.cut(df['hum'], bins=hum_bins, labels=hum_labels)

    # Visualisasi rata-rata jumlah pengguna berdasarkan kelembaban
    st.subheader("📊 Jumlah Pengguna Sepeda Berdasarkan Kelompok Kelembaban")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='hum_group', y=df['cnt'] / 1_000_000, data=df, estimator=sum, hue='hum_group', palette='coolwarm', ax=ax)
    ax.set_xlabel('Kelompok Kelembaban')
    ax.set_ylabel('Jumlah Pengguna Sepeda (Juta)')
    ax.set_title('Pengaruh Kelembaban terhadap Penggunaan Sepeda')
    st.pyplot(fig)

    # -----------------------------------------------

    # Heatmap Korelasi
    st.subheader("🔥 Korelasi antara Suhu, Kelembaban, dan Jumlah Pengguna Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df[['temp', 'hum', 'cnt']].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title('Korelasi antara Suhu, Kelembaban, dan Jumlah Pengguna Sepeda')
    st.pyplot(fig)

    # -----------------------------------------------

    # Bagian Keterangan Analisis
    st.subheader("📌 Kesimpulan Analisis:")
    st.markdown("""
    - 🚴 Pengguna sepeda lebih memilih suhu yang **hangat (24-32°C)** dan kelembaban yang **normal (0,4 - 0,6)** untuk bersepeda.
    - 🌡️ **Suhu** memiliki hubungan lebih kuat dengan jumlah pengguna sepeda (**0.26% korelasi**).
    - 💧 **Kelembaban** hampir tidak memengaruhi jumlah pengguna sepeda (**-0.24% korelasi**).
    - ❌ **Persentase korelasi** menunjukkan tingkat pengaruh suhu dan kelembaban sangat kecil terhadap jumlah pengguna sepeda.
    """)


if tab == "Apa perbedaan jumlah pengguna sepeda antara pengguna casual dan pengguna registered pada hari libur dan hari kerja?":
    # Hitung total pengguna casual dan registered berdasarkan hari kerja vs hari libur
    grouped_data = df.groupby('workingday')[['casual', 'registered']].sum()

    # Ubah index menjadi label
    grouped_data.index = ['Hari Libur', 'Hari Kerja']

    # Tampilkan subheader di Streamlit
    st.subheader("📊 Perbedaan Pengguna Sepeda: Casual vs Registered (Hari Libur vs Hari Kerja)")
    
    # Buat figure dan axis untuk plot
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.arange(len(grouped_data))
    width = 0.5  # Lebar batang

    # Plot Casual
    bars1 = ax.bar(x, grouped_data['casual'] / 1e6, color='skyblue', label='Casual', width=width)

    # Plot Registered di atas Casual
    bars2 = ax.bar(x, grouped_data['registered'] / 1e6, color='salmon', 
                bottom=grouped_data['casual'] / 1e6, label='Registered', width=width)

    # Tambahkan label jumlah pengguna di atas batang
    for bar, casual, registered in zip(bars1, grouped_data['casual'], grouped_data['registered']):
        ax.text(bar.get_x() + bar.get_width() / 2, 
                casual / 1e6 / 2,  # Posisi di tengah bar casual
                f'{casual / 1e6:.2f}', 
                ha='center', va='center', fontsize=10, color='black', fontweight='bold')

    for bar, casual, registered in zip(bars2, grouped_data['casual'], grouped_data['registered']):
        ax.text(bar.get_x() + bar.get_width() / 2, 
                (casual + registered) / 1e6 - (registered / 1e6 / 2),  # Posisi di tengah bar registered
                f'{registered / 1e6:.2f}', 
                ha='center', va='center', fontsize=10, color='black', fontweight='bold')

    # Tambahkan label dan judul
    ax.set_xticks(x)
    ax.set_xticklabels(grouped_data.index)
    ax.set_ylabel('Total Jumlah Pengguna (Juta)')
    ax.set_title('Perbedaan Pengguna Sepeda: Casual vs Registered\n(Hari Libur vs Hari Kerja)', fontsize=12)
    ax.legend()

    # Format sumbu y agar menampilkan angka dalam juta
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}'))

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

    # -----------------------------------------------

    # Bagian Keterangan Analisis
    st.subheader("📌 Kesimpulan Analisis:")
    st.markdown("""
    - 🚴 **Sebagian besar pengguna sepeda** di Washington D.C. adalah **registered users**, terutama di hari kerja.
    - 🏞️ **Pada hari libur**, jumlah **casual users meningkat**, kemungkinan karena mereka menggunakan sepeda untuk rekreasi.
    - 🚲 **Sepeda lebih sering digunakan sebagai moda transportasi utama di hari kerja**, bukan hanya sebagai aktivitas santai.
    - 📈 Untuk **optimasi layanan sepeda**, bisa dipertimbangkan:
        - 🚀 **Meningkatkan layanan** (jalur sepeda, jumlah sepeda) di hari kerja untuk **registered users**.
        - 🌳 **Meningkatkan fasilitas rekreasi** (jalur wisata, penyewaan fleksibel) di hari libur untuk **casual users**.
    """)


if tab == "Bagaimana Pola Penggunaan Sepeda dalam Sehari, terutama berdasarkan pengaruh cuaca?":
    
    # Hitung rata-rata jumlah pengguna per jam
    hourly_trend = df.groupby('hr')['cnt'].mean().reset_index()
    
    # Visualisasi tren per jam
    st.subheader("📊 Tren Penggunaan Sepeda Per Jam")

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='hr', y=hourly_trend['cnt'], data=hourly_trend, marker='o', color='r', ax=ax)

    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Jumlah Pengguna (Juta)')
    ax.set_title('Tren Penggunaan Sepeda Per Jam')
    ax.set_xticks(range(0, 24))
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

    # -----------------------------------------------

    # Kelompokkan berdasarkan jam dan kondisi cuaca, lalu hitung rata-rata jumlah pengguna sepeda
    hourly_weather = df.groupby(['hr', 'weathersit'])['cnt'].mean().reset_index()

    # Mapping kondisi cuaca ke label deskriptif
    weather_labels = {
        1: "Cerah / Berawan",
        2: "Berkabut / Mendung",
        3: "Hujan Ringan / Salju Ringan",
        4: "Hujan Lebat / Badai"
    }
    hourly_weather['weathersit'] = hourly_weather['weathersit'].map(weather_labels)

    # Visualisasi pola per jam berdasarkan cuaca
    st.subheader("⛅ Penggunaan Sepeda Berdasarkan Kondisi Cuaca")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=hourly_weather, hue='weathersit', marker='o', palette='coolwarm', ax=ax)

    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Jumlah Pengguna (Juta)')
    ax.set_title('Rata-rata Penggunaan Sepeda per Jam Berdasarkan Kondisi Cuaca')
    ax.set_xticks(range(0, 24))
    ax.legend(title='Kondisi Cuaca')
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

    # -----------------------------------------------

    # Bagian Keterangan Analisis
    st.subheader("📌 Kesimpulan Analisis:")
    st.markdown("""
    - 🕒 **Puncak penggunaan terjadi saat jam kerja (08:00 - 09:00) dan jam pulang kerja (17:00 - 18:00)**, menunjukkan bahwa sepeda adalah **alternatif transportasi utama** bagi banyak orang.
    - 🌧️ **Cuaca sangat berpengaruh terhadap jumlah pengguna**: Saat kondisi buruk seperti hujan lebat atau badai, **jumlah pengguna turun drastis**.
    - 🚲 Untuk **peningkatan infrastruktur**, dapat dipertimbangkan:
        - 🏗️ Membangun **jalur sepeda yang lebih aman** untuk meningkatkan kenyamanan pengguna.
        - ☔ **Tempat berteduh dan parkir sepeda yang terlindungi** untuk mendukung penggunaan sepeda bahkan saat cuaca kurang mendukung.
    """)


# Footer
st.markdown("---")
st.markdown("🚲 **Bike Sharing Dashboard** | Dibuat dengan ❤️ oleh Data Analyst")