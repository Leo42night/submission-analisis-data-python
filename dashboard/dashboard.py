import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    return df

df = load_data()

# Judul Dashboard
st.title("📊 Bike Sharing Dashboard")

# Sidebar untuk Filter Data
st.sidebar.header("🔍 Filter Data")

# Filter berdasarkan Tanggal
df['dteday'] = pd.to_datetime(df['dteday'])
start_date = df['dteday'].min()
end_date = df['dteday'].max()
selected_date = st.sidebar.date_input("Pilih Rentang Tanggal", [start_date, end_date], min_value=start_date, max_value=end_date)

# Filter berdasarkan Musim (Season)
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_label'] = df['season'].map(season_mapping)
selected_season = st.sidebar.multiselect("Pilih Musim", df['season_label'].unique(), default=df['season_label'].unique())

# Filter berdasarkan Kondisi Cuaca (Weathersit)
weather_mapping = {1: "Cerah / Berawan", 2: "Berkabut / Mendung", 3: "Hujan Ringan / Salju Ringan", 4: "Hujan Lebat / Badai"}
df['weathersit_label'] = df['weathersit'].map(weather_mapping)
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", df['weathersit_label'].unique(), default=df['weathersit_label'].unique())

# Terapkan Filter
df_filtered = df[(df['dteday'] >= pd.to_datetime(selected_date[0])) & 
                 (df['dteday'] <= pd.to_datetime(selected_date[1])) & 
                 (df['season_label'].isin(selected_season)) &
                 (df['weathersit_label'].isin(selected_weather))]

# Total pengguna setelah filter
total_users = df_filtered['cnt'].sum()
st.metric("🚴 Total Pengguna Setelah Filter:", f"{total_users:,}".replace(",", "."))


# Tampilkan data yang telah difilter
st.write("### Data yang Ditampilkan Setelah Filter")
st.dataframe(df_filtered.head())

# **1. Diagram Clustering Manual Grouping (Binning) Suhu vs Jumlah Pengguna**
temp_bins = [0, 8.2, 16.4, 24.6, 32.8, 41]
temp_labels = ['Sangat Dingin (0-8°C)', 'Dingin (8-16°C)', 'Normal (16-24°C)', 'Hangat (24-32°C)', 'Panas (32-41°C)']
df_filtered['temp_group'] = pd.cut(df_filtered['temp'] * 41, bins=temp_bins, labels=temp_labels)

st.subheader("📊 Jumlah Pengguna Sepeda Berdasarkan Kelompok Suhu")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='temp_group', y='cnt', data=df_filtered, estimator=sum, hue='temp_group', palette='coolwarm', ax=ax)
ax.set_xlabel('Kelompok Suhu')
ax.set_ylabel('Jumlah Pengguna Sepeda')
ax.set_title('Pengaruh Suhu terhadap Penggunaan Sepeda')
st.pyplot(fig)

# **2. Diagram Clustering Manual Grouping (Binning) Kelembaban**
hum_bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
hum_labels = ['Sangat Kering', 'Kering', 'Normal', 'Lembab', 'Sangat Lembab']
df_filtered['hum_group'] = pd.cut(df_filtered['hum'], bins=hum_bins, labels=hum_labels)

st.subheader("📊 Jumlah Pengguna Sepeda Berdasarkan Kelompok Kelembaban")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='hum_group', y='cnt', data=df_filtered, estimator=sum, hue='hum_group', palette='coolwarm', ax=ax)
ax.set_xlabel('Kelompok Kelembaban')
ax.set_ylabel('Jumlah Pengguna Sepeda')
ax.set_title('Pengaruh Kelembaban terhadap Penggunaan Sepeda')
st.pyplot(fig)

# **3. Diagram Total Pengguna Casual dan Registered Berdasarkan Hari Kerja vs Hari Libur**
grouped_data = df_filtered.groupby('workingday')[['casual', 'registered']].sum()
grouped_data.index = ['Hari Libur', 'Hari Kerja']

st.subheader("📊 Perbedaan Pengguna Sepeda: Casual vs Registered (Hari Libur vs Hari Kerja)")
fig, ax = plt.subplots(figsize=(8, 6))
x = np.arange(len(grouped_data))
width = 0.5
bars1 = ax.bar(x, grouped_data['casual'], color='skyblue', label='Casual', width=width)
bars2 = ax.bar(x, grouped_data['registered'], color='salmon', bottom=grouped_data['casual'], label='Registered', width=width)
ax.set_xticks(x)
ax.set_xticklabels(grouped_data.index)
ax.set_ylabel('Total Jumlah Pengguna')
ax.set_title('Perbedaan Pengguna Sepeda: Casual vs Registered')
ax.legend()
st.pyplot(fig)

# **4. Diagram Rata-rata Jumlah Pengguna Per Jam**
hourly_trend = df_filtered.groupby('hr')['cnt'].mean().reset_index()
st.subheader("📊 Tren Penggunaan Sepeda Per Jam")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(x='hr', y='cnt', data=hourly_trend, marker='o', color='r', ax=ax)
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Pengguna')
ax.set_title('Tren Penggunaan Sepeda Per Jam')
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

# **5. Diagram Rata-rata Pengguna yang dikelompokkan berdasarkan Jam dan Kondisi Cuaca**
hourly_weather = df_filtered.groupby(['hr', 'weathersit_label'])['cnt'].mean().reset_index()
st.subheader("⛅ Penggunaan Sepeda Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_weather, hue='weathersit_label', marker='o', palette='coolwarm', ax=ax)
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Pengguna')
ax.set_title('Rata-rata Penggunaan Sepeda per Jam Berdasarkan Kondisi Cuaca')
ax.set_xticks(range(0, 24))
ax.legend(title='Kondisi Cuaca')
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.markdown("---")
st.markdown("🚲 **Bike Sharing Dashboard** | Dibuat dengan ❤️ oleh Data Analyst")
