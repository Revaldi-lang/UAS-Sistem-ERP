# -*- coding: utf-8 -*-
{
    'name': 'Kemuning Dynamic Florist',
    'version': '17.0.5.0.0',
    'category': 'Inventory/Sales/Point of Sale/Manufacturing/Human Resources',
    'summary': 'Modul Kustom Odoo 17 untuk Toko Bunga Kemuning Florist',
    'description': """
        Modul kustom Odoo 17 untuk mendigitalkan operasional Kemuning Florist:
        - Dasbor Harga Harian (Dynamic Pricing)
        - Sistem Warna Peringatan Umur Bunga (Color-Coded Inventory)
        - Status Bunga Impor vs Lokal
        - Integrasi Laporan Penjualan & Laporan Kasir POS (Bunga Impor vs Lokal)
        - Dashboard KPI Interaktif (Kanban, Grafik, List)
        - Dasbor Analitik / BI Dashboard (Penyatuan Grafik Laporan)
        - Kategori Inspeksi QC (qc.test.category)
        - Sistem Titik Kontrol Kualitas & Pemeriksaan Fisik QC Mandiri (Community-compatible)
        - Role-Based Access Control (Kasir, Admin, Manajer)
        
        Memenuhi seluruh syarat minimum master data penugasan Proyek Akhir Sistem ERP.
    """,
    'author': 'Nayla Dwinta Putri Muharram, Oreza Sativa Wibowo, Revaldi Firdaus',
    'website': 'https://www.upnvj.ac.id',
    'depends': ['product', 'stock', 'product_expiry', 'sale', 'point_of_sale', 'board', 'mrp', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/stock_lot_views.xml',
        'views/daily_pricing_dashboard_views.xml',
        'views/kemuning_kpi_views.xml',
        'views/kemuning_bi_dashboard.xml',
        'views/qc_test_category_views.xml',
        'views/qc_quality_views.xml',
        'views/menus.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
