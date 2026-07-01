# 🌸 ERP Customization & Configuration - Kemuning Florist

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0%20Community%2FEnterprise-purple.svg)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)
[![Category](https://img.shields.io/badge/Category-Inventory%20%2F%20Sales%20%2F%20Manufacturing-orange.svg)](#)

Repositoy ini berisi modul kustom Odoo 17 (**`kemuning_dynamic_florist`**) dan file konfigurasi sistem ERP untuk digitalisasi operasional toko bunga **Kemuning Florist**. Modul kustom ini dikembangkan untuk memenuhi kebutuhan integrasi lintas departemen (Pembelian, Inventaris, Produksi/Assembly, Penjualan, POS, QC, dan Keuangan) serta dilengkapi dengan fitur *Dynamic Pricing* dan sistem pemantauan kesegaran bunga berbasis warna.

---

## 📌 Daftar Isi
1. [Deskripsi Proyek](#-deskripsi-proyek)
2. [Fitur Utama Modul Custom](#-fitur-utama-modul-custom)
3. [Struktur Folder & Berkas Penting](#-struktur-folder--berkas-penting)
4. [Master Data & Skenario Awal (Demo Data)](#-master-data--skenario-awal-demo-data)
5. [Panduan Instalasi Modul](#-panduan-instalasi-modul)
6. [User Guide (Panduan Operasional Pengguna)](#-user-guide-panduan-operasional-pengguna)
7. [Keamanan & Hak Akses (Role-Based Access Control)](#-keamanan--hak-akses-role-based-access-control)

---

## 🌸 Deskripsi Proyek

**Kemuning Florist** adalah toko bunga yang menjual bunga potong segar (lokal dan impor) serta karangan bunga/bucket (*finished goods*). Karakteristik utama dari bisnis bunga segar adalah **fluktuasi harga pasar harian** yang sangat dinamis dan **umur simpan produk (perishable)** yang sangat pendek (biasanya 3-5 hari).

Modul **`kemuning_dynamic_florist`** menjembatani keterbatasan standar Odoo dengan menyediakan:
- Mekanisme pembaruan harga jual secara massal setiap pagi mengikuti harga pasar.
- Peringatan visual (warna) di gudang/kasir untuk lot bunga yang hampir layu.
- Sistem Penjaminan Kualitas (Quality Control) mandiri tanpa harus membeli lisensi Odoo Enterprise.
- Visualisasi dasbor KPI instan dan laporan analitik (BI) terpadu.

---

## 🛠️ Fitur Utama Modul Custom

### 1. Dasbor Harga Harian (Dynamic Pricing)
- Memungkinkan tim Admin/Manajer memasukkan **Harga Jual Hari Ini** pada daftar bunga segar secara cepat dalam format tabel *editable* (Excel-like).
- Menyediakan tombol **"Terapkan Harga Hari Ini"** untuk menyalin harga harian tersebut ke harga jual standar (`list_price`) secara massal. Harga ini otomatis langsung aktif di kasir POS dan modul Penjualan.

### 2. Sistem Warna Peringatan Umur Bunga (Color-Coded Inventory)
- Menggunakan data *Lot/Serial Number* dan *Expiration Date* bawaan Odoo untuk mendeteksi sisa hari kesegaran bunga.
- Memberikan pewarnaan otomatis pada baris lot di menu inventaris:
  - 🔴 **Merah (Danger)**: Jika sisa umur bunga $\le$ 24 jam (hampir/sudah layu).
  - 🟡 **Kuning/Oranye (Warning)**: Jika sisa umur bunga berkisar antara 1 sisa hari hingga 3 hari.
  - ⚪ **Putih/Default**: Jika bunga masih sangat segar (> 3 hari).

### 3. Status Asal Bunga (Impor vs Lokal) & Integrasi Laporan
- Menambahkan bendera penanda **"Bunga Impor?"** pada produk.
- Mengintegrasikan status ini ke dalam basis data **Laporan Penjualan Penjualan (Sales)** dan **Laporan Penjualan Kasir (POS)**. Pemilik toko dapat melihat visualisasi pivot/grafik perbandingan performa penjualan bunga impor vs bunga lokal.

### 4. Sistem QC & Pemeriksaan Fisik Mandiri (Community-Compatible)
- Menyediakan fitur pembuatan **Kategori Uji QC** (`qc.test.category`) secara hierarkis.
- Menyediakan tabel **Titik Pemeriksaan QC** (`qc.quality.point`) untuk mendefinisikan instruksi pengujian pada setiap produk bunga segar.
- Menyediakan lembar kerja **Pemeriksaan Kelayakan QC** (`qc.quality.check`) untuk mencatat log pengujian fisik bunga (Draft $\rightarrow$ Pass / Fail) beserta catatan kondisi fisiknya.

### 5. Dasbor KPI & Analitik BI Terintegrasi
- **Dasbor KPI Utama**: Kartu Kanban interaktif yang menyajikan metrik penting secara *real-time*:
  - *Total Variasi Bunga*: Jumlah jenis bunga segar aktif.
  - *Proporsi Bunga Impor*: Persentase bunga impor terhadap seluruh variasi bunga.
  - *Bunga Hampir Layu*: Jumlah lot bunga aktif yang memiliki sisa umur $\le$ 24 jam.
  - *Total Penjualan Bunga*: Gabungan nilai penjualan dari modul Sales (SO) dan POS.
- **Dasbor Analitik (BI)**: Penyatuan grafik laporan Odoo Board yang menggabungkan:
  - Grafik Pivot penjualan modul Sales.
  - Grafik Bar penjualan modul Kasir POS.
  - List pemantauan sisa umur bunga segar di gudang.

---

## 📂 Struktur Folder & Berkas Penting

Modul kustom dikemas dalam satu folder addon `kemuning_dynamic_florist`. Berikut adalah berkas-berkas penting yang membentuk modul ini:

```text
kemuning_dynamic_florist/
├── __init__.py
├── __manifest__.py                 # Deklarasi metadata modul, dependensi, dan urutan file data/views
├── data/
│   └── demo_data.xml               # Master data lengkap & skenario awal (kategori, produk, BoM, partner, KPI)
├── models/
│   ├── __init__.py
│   ├── product_template.py         # Kustomisasi objek Product (Harga Harian, Asal Bunga, Bersihkan Demo Data)
│   ├── stock_lot.py                # Perhitungan sisa hari layu dan status hampir kadaluwarsa
│   ├── sale_report.py              # Injeksi field 'is_imported' ke database view Laporan Sales
│   ├── pos_order_report.py         # Injeksi field 'is_imported' ke database view Laporan POS
│   ├── kemuning_kpi.py             # Logika kalkulasi matematis/OR-Query untuk 4 indikator KPI utama
│   ├── qc_test_category.py        # Pengaturan kategori inspeksi QC bertingkat
│   └── qc_quality.py               # Model untuk Quality Control Points & Quality Control Checks
├── security/
│   ├── security.xml                # Konfigurasi Group Hak Akses (Kasir, Admin, Pemilik/Manajer)
│   └── ir.model.access.csv         # Matriks perizinan database (Access Control List) untuk model baru
├── views/
│   ├── menus.xml                   # Hierarki Menu Utama & Sub-menu Kemuning Florist di Odoo
│   ├── product_template_views.xml  # Inherit form produk untuk menampilkan flag kustom bunga
│   ├── stock_lot_views.xml         # Inherit list stock lot untuk implementasi pewarnaan merah/kuning
│   ├── daily_pricing_dashboard_views.xml # Form Excel-like untuk input harga harian & tombol aksi massal
│   ├── kemuning_kpi_views.xml      # Layout Kanban Card & Graph View untuk dashboard KPI
│   ├── kemuning_bi_dashboard.xml   # Penyatuan grafik-grafik dalam layout Odoo Board (BI)
│   ├── qc_test_category_views.xml  # Layout view Kategori QC
│   └── qc_quality_views.xml        # Layout view dan tombol aksi Lolos/Gagal Uji QC
└── static/
    └── description/
        └── icon.png                # Ikon menu utama modul Kemuning Florist
```

### File Tautan Cepat (Akses Lokal):
- 📄 [__manifest__.py](file:///c:/Users/user/OneDrive/Desktop/UAS%20ERP/09_Customization/Source_Code_or_Config/kemuning_dynamic_florist/__manifest__.py)
- 📄 [models/product_template.py](file:///c:/Users/user/OneDrive/Desktop/UAS%20ERP/09_Customization/Source_Code_or_Config/kemuning_dynamic_florist/models/product_template.py)
- 📄 [models/stock_lot.py](file:///c:/Users/user/OneDrive/Desktop/UAS%20ERP/09_Customization/Source_Code_or_Config/kemuning_dynamic_florist/models/stock_lot.py)
- 📄 [views/menus.xml](file:///c:/Users/user/OneDrive/Desktop/UAS%20ERP/09_Customization/Source_Code_or_Config/kemuning_dynamic_florist/views/menus.xml)
- 📄 [security/security.xml](file:///c:/Users/user/OneDrive/Desktop/UAS%20ERP/09_Customization/Source_Code_or_Config/kemuning_dynamic_florist/security/security.xml)
- 📄 [data/demo_data.xml](file:///c:/Users/user/OneDrive/Desktop/UAS%20ERP/09_Customization/Source_Code_or_Config/kemuning_dynamic_florist/data/demo_data.xml)

---

## 📦 Master Data & Skenario Awal (Demo Data)

Saat modul diinstal pertama kali, sistem akan memuat data awal (**[demo_data.xml](file:///c:/Users/user/OneDrive/Desktop/UAS%20ERP/09_Customization/Source_Code_or_Config/kemuning_dynamic_florist/data/demo_data.xml)**) yang secara otomatis memenuhi seluruh syarat minimum master data ujian:

| Kategori Data | Nama Record / Detail Master Data | Kegunaan dalam Sistem |
| :--- | :--- | :--- |
| **Kategori Produk** | Bunga Segar, Bahan Baku Florist, Bucket Bunga Jadi, Bucket Custom, Paket Spesial | Struktur pengelompokan barang dagangan |
| **Bahan Baku (Raw)** | - Bunga Mawar Merah Lokal (Storable, Lot tracking, Expiry aktif)<br>- Bunga Lili Kuning Lokal (Storable, Lot tracking, Expiry aktif)<br>- Kertas Wrapping Transparan (Storable)<br>- Pita Satin Merah (Storable) | Digunakan sebagai stok bunga potong segar & bahan merangkai |
| **Produk Jadi** | - Bucket Bunga Mawar Merah Cantik (tracked)<br>- Bucket Bunga Lili Kuning Spesial (tracked) | Produk akhir yang dirangkai dan dijual ke konsumen |
| **Work Center** | Meja Perakitan & Rangkaian Bunga (Biaya: Rp15.000 / jam) | Stasiun kerja tempat karyawan merangkai karangan bunga |
| **Bill of Materials (BoM)**| - BoM Bucket Mawar: 5 tangkai Mawar + 1 Kertas + 1 Pita<br>- BoM Bucket Lili: 5 tangkai Lili + 1 Kertas + 1 Pita | Resep fabrikasi produk jadi di modul Manufacturing (MRP) |
| **Mitra (Partners)** | - Supplier: Kebun Bunga Mawar Nusantara, Distributor Kertas & Aksesoris<br>- Customer: Ibu Rina Wijaya, Bapak Budi Santoso | Data entitas luar untuk proses Purchase & Sales |
| **Karyawan (HR)** | - Ahmad Hidayat (Manajer)<br>- Siti Aminah (Staf Pembuat/Rangkai)<br>- Dewi Lestari (Kasir Shift Depan) | Data staf internal untuk pembagian kerja dan otorisasi |
| **Quality Control** | QC Point: *"Inspeksi Kesegaran & Umur Kelopak Bunga Mawar"* pada produk Mawar Merah. | Acuan standar kualitas saat penerimaan bunga masuk |
| **KPI Dashboard** | Record untuk Variasi, Impor, Expiring, dan Sales | Tempat penampung data visualisasi Kanban KPI |

---

## ⚙️ Panduan Instalasi Modul

### Prasyarat (Requirements):
1. Menggunakan **Odoo versi 17** (Community Edition atau Enterprise Edition).
2. Memastikan modul-modul standar berikut sudah terpasang di database Odoo Anda:
   - `product` (Produk)
   - `stock` (Persediaan/Inventory)
   - `product_expiry` (Pelacakan Kadaluwarsa Produk)
   - `sale` (Penjualan/Sales)
   - `point_of_sale` (POS)
   - `board` (Dashboard Builder)
   - `mrp` (Manufaktur/Manufacturing)
   - `hr` (Karyawan/Human Resources)

### Langkah-Langkah Instalasi:
1. Salin folder `kemuning_dynamic_florist` ke dalam direktori addons Odoo Anda (misal: `odoo/addons/` atau direktori custom addons Anda).
2. Nyalakan **Developer Mode** di database Odoo (Settings $\rightarrow$ General Settings $\rightarrow$ Scroll ke bawah, klik *Activate the developer mode*).
3. Buka menu **Apps** di Odoo.
4. Klik tombol **"Update Apps List"** di bagian atas menu navigasi agar Odoo memindai modul baru.
5. Ketik `"Kemuning Dynamic Florist"` di kolom pencarian (hapus filter *Apps* bawaan terlebih dahulu).
6. Klik **Activate** pada modul Kemuning Dynamic Florist. Odoo akan menginstal modul beserta demo data bawaannya secara otomatis.

---

## 📖 User Guide (Panduan Operasional Pengguna)

> [!IMPORTANT]
> Ikuti panduan ini langkah-demi-langkah untuk mendemonstrasikan proses bisnis utama Kemuning Florist kepada penguji atau pengguna akhir.

### Alur Kerja 1: Pembersihan Data Demo Bawaan Odoo (Clean Demo Data)
Saat database Odoo baru diinstal, biasanya terdapat banyak data demo bawaan (seperti produk meja, kursi, transaksi dummy, dll) yang mengotori dasbor laporan. Modul ini menyediakan fungsi pembersihan khusus.

1. Buka menu **Kemuning Florist** $\rightarrow$ klik sub-menu **Dasbor Harga Harian**.
2. Di bagian atas tabel, klik tombol **"Bersihkan Data Demo Odoo"** berwarna merah.
3. Konfirmasikan tindakan.
4. **Hasil**: Database Anda kini bersih dari data transaksi dummy Odoo, produk furnitur, dan lot bawaan. Hanya master data eksklusif **Kemuning Florist** (Mawar, Lili, Pita, Karyawan Kemuning, dsb) yang tersisa.

---

### Alur Kerja 2: Manajemen Harga Harian (Dynamic Pricing)
Bunga segar harganya berubah setiap pagi tergantung pasokan petani. Lakukan simulasi pembaruan harga berikut:

1. Buka menu **Kemuning Florist** $\rightarrow$ **Dasbor Harga Harian**.
2. Anda akan melihat daftar bunga segar dalam mode baris tabel yang dapat diedit langsung (*inline editing*).
3. Isi kolom **Harga Jual Hari Ini (Fluktuatif)**. Contoh:
   - Bunga Mawar Merah Lokal: Ubah dari Rp15.000 menjadi **Rp18.000**.
   - Bunga Lili Kuning Lokal: Ubah dari Rp22.000 menjadi **Rp25.000**.
4. Klik tombol **"Terapkan Harga Hari Ini"** di header tabel.
5. Konfirmasikan pop-up pengingat.
6. **Hasil**: Notifikasi sukses akan muncul. Sistem akan menyalin nilai tersebut ke kolom **Harga Jual Kasir (Aktif)** (`list_price`). Jika Anda membuka kasir Point of Sale (POS) atau modul Sales sekarang, harga produk otomatis ter-update menjadi Rp18.000 & Rp25.000 secara instan!

---

### Alur Kerja 3: Pemantauan Umur Bunga & Indikator Warna (Color-Coded Inventory)
Toko ingin memastikan bunga yang sudah layu tidak terjual ke pelanggan.

1. Buka menu **Kemuning Florist** $\rightarrow$ **Pemantauan Umur Bunga**.
2. Anda akan melihat daftar Lot/Serial Number dari bunga yang sedang disimpan di gudang.
3. Perhatikan pewarnaan baris:
   - **Baris Merah (Danger)**: Menandakan bunga tersebut memiliki **Hari Menuju Layu = 0** atau **1** (sisa waktu hidup $\le$ 24 jam). Harus segera digunakan untuk diskon cuci gudang atau dibuang.
   - **Baris Kuning/Oranye (Warning)**: Menandakan bunga memiliki sisa waktu hidup **2 hingga 3 hari**. Perlu diprioritaskan untuk dirangkai terlebih dahulu (sistem FEFO - *First Expired First Out*).
4. Kolom **"Hari Menuju Layu"** dikalkulasi secara otomatis oleh sistem dengan membandingkan waktu saat ini dengan kolom *Tanggal Kadaluwarsa (Expiration Date)* pada Lot tersebut.

---

### Alur Kerja 4: Prosedur Pemeriksaan Kualitas (QC Check)
Sebelum bunga masuk ke gudang penyimpanan utama atau dirangkai menjadi bucket, staf harus melakukan QC fisik.

1. Buka menu **Kemuning Florist** $\rightarrow$ **Pemeriksaan Kelayakan QC**.
2. Klik tombol **New (Buat Baru)**.
3. Isi data pemeriksaan:
   - **Kode Inspeksi**: Otomatis terisi (atau ketik nomor referensi Anda).
   - **Titik Kontrol**: Pilih *"Inspeksi Kesegaran & Umur Kelopak Bunga Mawar"* (QC Point yang terdaftar).
   - **Produk Terkait**: Pilih *Bunga Mawar Merah Lokal*.
   - **Nomor Lot/Serial**: Pilih lot bunga mawar yang sedang diperiksa.
   - **Catatan**: Tulis hasil pengujian fisik (misal: *"Kelopak bersih, batang kokoh, siap dirangkai"*).
4. Di bagian header formulir:
   - Klik **Lolos Uji (Pass)** jika bunga memenuhi kualifikasi. Status akan berubah menjadi hijau **Lolos Uji (Pass)**.
   - Klik **Gagal Uji (Fail)** jika bunga layu atau patah. Status akan berubah menjadi merah **Gagal Uji (Fail)**.
5. **Hasil**: Log pemeriksaan ini tersimpan rapi untuk audit performa supplier dan QC internal.

---

### Alur Kerja 5: Membuka KPI & Analitik BI Dashboard
Pemilik ingin memantau kesehatan bisnis Kemuning Florist secara cepat.

#### **Melihat Dashboard Utama (KPI)**
1. Buka menu **Kemuning Florist** $\rightarrow$ **Dashboard Utama**.
2. Sistem akan menyajikan kartu Kanban interaktif dengan metrik *real-time*:
   - Menampilkan total jenis bunga terdaftar.
   - Menampilkan proporsi persentase bunga impor (misal: "0 Impor dari 4 (0.0%)" jika tidak ada bunga impor).
   - Menampilkan jumlah lot bunga yang hampir layu ($\le$ 24 jam) untuk segera di-follow up.
   - Menampilkan akumulasi nilai rupiah penjualan bunga dari modul Sales & POS.
3. Anda dapat mengklik tombol **Graph View** (ikon grafik di kanan atas) untuk menyajikan perbandingan metrik dalam bentuk diagram batang.

#### **Melihat Dasbor Analitik (BI)**
1. Buka menu **Kemuning Florist** $\rightarrow$ **Dasbor Analitik (BI)**.
2. Halaman ini menyatukan 3 laporan sekaligus:
   - **Sisi Kiri Atas**: Pivot Analisis Penjualan Sales (Modul Penjualan Grosir/WA).
   - **Sisi Kiri Bawah**: Grafik Batang Analisis Penjualan Kasir POS.
   - **Sisi Kanan**: Daftar Detail Pemantauan Umur Bunga (Lot).
3. Anda dapat melakukan filter dan export data ke excel langsung dari satu dasbor tunggal ini.

---

## 👥 Keamanan & Hak Akses (Role-Based Access Control)

Modul ini membatasi akses demi keamanan operasional kasir dan integritas data keuangan:

1. **Kasir Depan (`group_florist_cashier`)**:
   - *Hak Akses*: Hanya bisa menggunakan modul Point of Sale (POS) untuk bertransaksi dan melihat menu **Pemantauan Umur Bunga** serta melakukan **Pemeriksaan Kelayakan QC** (untuk melaporkan bunga rusak di kasir).
   - *Batasan*: **TIDAK BISA** melihat atau mengubah Harga Jual Hari Ini di Dasbor Harga Harian, tidak bisa melihat laporan keuangan utama, dan tidak bisa menghapus data transaksi.

2. **Staf Admin (`group_florist_admin`)**:
   - *Hak Akses*: Mewarisi seluruh hak Kasir. Ditambah kemampuan mengedit data produk, memperbarui **Harga Jual Hari Ini**, menjalankan proses manufaktur (merangkai bunga), dan melihat Laporan Penjualan.
   - *Batasan*: Tidak diizinkan melakukan penghapusan data transaksi secara permanen.

3. **Pemilik / Manajer Utama (`group_florist_manager`)**:
   - *Hak Akses*: Mewarisi seluruh hak Staf Admin. Memiliki hak penuh (*super-user*) termasuk menjalankan tombol **"Bersihkan Data Demo Odoo"**, memodifikasi kategori QC, dan melihat seluruh dasbor KPI/BI keuangan.

> [!TIP]
> Untuk menguji hak akses ini, masuk ke menu **Settings** $\rightarrow$ **Users & Companies** $\rightarrow$ **Users**. Pilih salah satu user, lalu cari kategori **Kemuning Florist** di bagian bawah dan ubah tingkat hak aksesnya (Kasir Depan, Staf Admin, atau Pemilik).

---
*Dikembangkan oleh Nayla Dwinta Putri Muharram, Oreza Sativa Wibowo, dan Revaldi Firdaus untuk Proyek Sistem ERP UPN Veteran Jakarta.*
