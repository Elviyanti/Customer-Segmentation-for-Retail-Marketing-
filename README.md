# Customer Segmentation for Personalized Retail Marketing
**Best Capstone Project — Asah led by Dicoding in association with Accenture**
Capstone project Machine Learning yang membangun segmentasi pelanggan ritel online menggunakan pendekatan **RFM (Recency, Frequency, Monetary)** dan **K-Means Clustering** dengan **PCA** sebagai tahap dimensionality reduction, untuk mendukung strategi pemasaran yang lebih personal, efisien, dan berdampak langsung pada retensi serta pendapatan.

> Proyek ini terpilih sebagai **Best Capstone Project** untuk use case Customer Segmentation for Personalized Retail Marketing.

---

## Ringkasan Proyek
Perusahaan ritel online seringkali menjalankan kampanye promosi yang sama ke seluruh pelanggan tanpa memperhatikan perbedaan perilaku belanja, sehingga promosi menjadi kurang efektif, biaya pemasaran meningkat, dan engagement pelanggan rendah.

Proyek ini menjawab dua pertanyaan utama:
- Bagaimana cara mengelompokkan pelanggan berdasarkan nilai dan perilaku belanjanya?
- Strategi pemasaran apa yang paling tepat untuk setiap kelompok pelanggan yang terbentuk?

Dengan menggabungkan fitur RFM dan algoritma clustering, pelanggan dikelompokkan ke dalam **3 segmen utama**:

| Segmen | Karakteristik |
|---|---|
| **Loyal** | Pelanggan aktif dengan frekuensi & nilai transaksi tinggi |
| **Potential** | Pelanggan dengan potensi nilai yang masih bisa ditingkatkan |
| **Churn** | Pelanggan pasif / berisiko berhenti bertransaksi |

Setiap segmen dilengkapi persona singkat dan rekomendasi strategi pemasaran (program loyalitas, promosi reaktivasi, welcome promo, penawaran produk premium, dll).

---

## Metodologi
1. **Data Preparation** — cleaning data (missing values, duplikasi, outlier, data negatif) serta dokumentasi proses pembersihan.
2. **Feature Engineering** — pembentukan fitur RFM (Recency, Frequency, Monetary) dari data transaksi.
3. **Dimensionality Reduction** — Principal Component Analysis (PCA) untuk mengurangi kompleksitas data dan korelasi antar fitur sebelum clustering.
4. **Modeling & Clustering** — perbandingan beberapa algoritma (K-Means, GMM, Agglomerative); K-Means + PCA dipilih berdasarkan performa evaluasi terbaik.
5. **Evaluation** — penentuan jumlah cluster optimal menggunakan **Elbow Method** dan **Silhouette Score**.
6. **Interpretation & Strategy** — interpretasi karakteristik tiap cluster menjadi persona pelanggan dan rekomendasi strategi pemasaran.
7. **Deployment** — dashboard interaktif menggunakan Streamlit untuk visualisasi hasil segmentasi.

### Hasil Evaluasi Model
K-Means + PCA (n_components = 2) = **0.6703** 
K-Means dengan PCA terbukti memberikan hasil clustering yang paling stabil, jelas, dan mudah diinterpretasikan dibandingkan model pembanding lainnya.

---

## Tech Stack
- **Bahasa Pemrograman:** Python
- **Data Processing:** Pandas, NumPy
- **Modeling & Evaluation:** Scikit-learn (K-Means, PCA, GMM, Agglomerative Clustering)
- **Visualisasi:** Matplotlib, Seaborn, Plotly
- **Dashboard / Prototyping:** Streamlit
- **Environment:** Google Colab

---

## Dataset

Dataset yang digunakan adalah **Online Retail Dataset** dari Kaggle, berisi data transaksi retail yang digunakan untuk eksplorasi data, pembersihan data, serta proses segmentasi pelanggan.

🔗 [Online Retail Dataset — Kaggle](https://www.kaggle.com/datasets/vijayuv/onlineretail)
1. Masuk ke link Demo
2. Masukkan CSV rfm_clustered (untuk melihat dashbaord visualisasinya

---

## Demo & Dashboard

Hasil segmentasi diimplementasikan dalam bentuk dashboard interaktif berbasis Streamlit, menyajikan executive summary, cluster profiling, RFM distribution, snake plot analysis, visualisasi 3D & PCA view, hingga fitur filter & export data.

🔗 **Live Demo:** [customer-segmentation-retail-dashboard.streamlit.app](https://customer-segmentation-retail-dashboard.streamlit.app/)

---

## Tim

Capstone Project **A25-CS279** — Machine Learning Path

| Nama | Role |
|---|---|
| Angel Calllista Pramadio | Machine Learning — Data Preprocessing & Feature Engineering |
| Elviyanti | Machine Learning — Modeling & Clustering |
| Farhan Ainurrahman | Machine Learning — Visualisasi, Interpretasi & Strategi Pemasaran |

**Advisor:** Aditya Aulia Al Azizi

---

## Struktur Repository

```
.
├── data/                 # Dataset mentah & hasil preprocessing
├── notebooks/            # Notebook EDA, preprocessing, modeling, evaluasi
├── dashboard/            # Source code dashboard Streamlit
├── reports/              # Laporan & dokumentasi pendukung
└── README.md
```

> Sesuaikan struktur folder di atas dengan struktur aktual pada repository ini.

---

## Insight & Rekomendasi Bisnis

- **Loyal Customers** → pertahankan dengan program loyalitas dan penawaran eksklusif.
- **Potential Customers** → dorong frekuensi transaksi melalui promosi yang dipersonalisasi dan cross-selling.
- **Churn Risk Customers** → lakukan kampanye reaktivasi dengan insentif khusus untuk mengembalikan engagement.

Pendekatan ini memungkinkan strategi pemasaran yang lebih tepat sasaran dibandingkan kampanye generik untuk seluruh pelanggan, sekaligus berpotensi menekan biaya promosi dan meningkatkan retensi.

---

## Acknowledgement

Proyek ini merupakan bagian dari program **Asah** yang diselenggarakan oleh **Dicoding** bekerja sama dengan **Accenture**.

---

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dalam program Capstone Asah x Dicoding x Accenture.
