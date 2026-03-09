# Stock Selection for Pair Trading

Project ini melakukan seleksi pasangan saham per sektor di IDX menggunakan 3 metode:
- Pearson Correlation
- Spearman Correlation
- Cointegration Test

## Alur Proses
1. Download data harga saham per sektor dari Yahoo Finance.
2. Cleaning dan preprocessing data.
3. Hitung semua kombinasi pasangan saham untuk:
   - Pearson
   - Spearman
   - Cointegration
4. Seleksi top pairs.
5. Simpan hasil ke file Excel di folder `result/`.

## Estimasi Waktu Proses
- Proses penuh biasanya memakan waktu sekitar **7-10 menit**.
- Waktu bisa lebih lama tergantung koneksi internet dan jumlah ticker yang berhasil terunduh.

## Output Hasil
Saat menjalankan `main.py`, sistem akan membuat file:
- `result/hasil_korelasi_<timestamp>.xlsx`

Isi file Excel terdiri dari beberapa sheet, misalnya:
- `pearson_all`
- `spearman_all`
- `cointegration_all`
- `selected_pairs`
- `summary_top`
- `top_pearson`
- `top_spearman`
- `top_cointegration`

Catatan:
- Jumlah baris hasil bisa **sangat banyak** karena semua kombinasi pair dihitung per sektor.

## Cara Membaca Hasil
### 1) Pearson Correlation
- Nilai correlation berada di rentang `-1` sampai `1`.
- Untuk pair trading biasanya dilihat pasangan dengan:
  - **nilai paling besar** (mendekati `1`) untuk hubungan positif paling kuat.
  - **nilai paling kecil** (mendekati `-1`) jika ingin melihat hubungan negatif paling kuat.
- Jika fokus ke pergerakan yang searah, gunakan nilai Pearson yang paling tinggi.

### 2) Spearman Correlation
- Sama-sama di rentang `-1` sampai `1`, tapi berbasis ranking (lebih tahan terhadap outlier).
- Interpretasi umum:
  - **semakin besar nilainya** -> monotonic relationship makin kuat.
  - **semakin kecil (negatif)** -> hubungan monotonic berlawanan arah.

### 3) Cointegration (P-Value)
- Fokus utama ada di `P_Value`.
- **Semakin kecil p-value**, semakin kuat indikasi pasangan cointegrated.
- Untuk pair trading, pasangan dengan p-value paling kecil biasanya jadi kandidat utama.

## Menjalankan Project
```bash
pip install -r requirements.txt
python main.py
```

## Dependensi Utama
- pandas
- numpy
- yfinance
- statsmodels
- openpyxl
