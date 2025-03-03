# Bike Trend Dashboard ✨
Informasi cara menjalankan dashoard.

## Setup Environment 
Lokasi di dalam folder project `submission-analisis-data-python/` dengan
file `requirement.txt` di dalamnya. Ada 2 pilihan instalasi (Anaconda atau Terminal)

### Anaconda
```
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
```

### Terminal

```
python -m venv myenv

# Windows
myenv\Scripts\activate

# macOS and Linux
source myenv/bin/activate

pip install -r requirements.txt
```

## Run steamlit app
Setelah setup install package dari `reqirements.txt` selesai. Dalam project folder, jalankan:
```
streamlit run dashboard/dashboard.py
```