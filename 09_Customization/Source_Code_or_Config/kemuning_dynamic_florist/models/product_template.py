# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_flower = fields.Boolean(
        string="Bunga Segar?",
        default=True,
        help="Centang jika produk ini merupakan bunga segar yang dapat layu."
    )
    daily_market_price = fields.Float(
        string="Harga Jual Hari Ini",
        digits='Product Price',
        help="Harga pasar harian yang fluktuatif untuk hari ini saja."
    )
    lifespan_days = fields.Integer(
        string="Batas Waktu Layu (Hari)",
        default=3,
        help="Daya tahan atau jatah umur bunga segar dalam hitungan hari."
    )
    is_imported = fields.Boolean(
        string="Bunga Impor?",
        default=False,
        help="Centang jika bunga didatangkan/diimpor dari luar negeri."
    )

    def action_apply_daily_prices(self):
        """Menyalin Harga Jual Hari Ini ke Harga Jual Standar secara massal"""
        # Jika user tidak mencentang baris mana pun, ambil semua bunga segar secara otomatis
        targets = self if self else self.search([('is_flower', '=', True)])
        updated_count = 0
        for product in targets:
            if product.is_flower and product.daily_market_price > 0.0:
                product.list_price = product.daily_market_price
                updated_count += 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Pembaruan Harga Berhasil',
                'message': f'Berhasil menerapkan harga harian untuk {updated_count} produk bunga.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_clean_demo_data(self):
        """Menghapus data demo bawaan Odoo secara bersih menggunakan SQL query langsung"""
        # 1. Hapus transaksi penjualan (POS & Sales)
        self.env.cr.execute("TRUNCATE pos_order_line, pos_order, pos_session CASCADE;")
        self.env.cr.execute("TRUNCATE sale_order_line, sale_order CASCADE;")
        self.env.cr.execute("TRUNCATE purchase_order_line, purchase_order CASCADE;")
        self.env.cr.execute("TRUNCATE mrp_production, mrp_bom_line, mrp_bom CASCADE;")
        self.env.cr.execute("TRUNCATE stock_quant, stock_move_line, stock_move, stock_valuation_layer, stock_lot CASCADE;")
        self.env.cr.execute("TRUNCATE account_move_line, account_move CASCADE;")
        
        # 2. Cari ID kategori Kemuning Florist agar tidak terhapus
        cats = self.env['product.category'].search([('name', 'in', ['Bunga Segar', 'Bahan Baku Florist', 'Bucket Bunga Jadi', 'Bucket Custom', 'Paket Spesial'])])
        cat_ids = list(cats.ids)
        
        # Jika ada kategori kemuning, hapus semua produk diluar kategori tersebut
        if cat_ids:
            cat_list = ','.join(map(str, cat_ids))
            # Hapus varian produk diluar kategori kemuning
            self.env.cr.execute(f"DELETE FROM product_product WHERE product_tmpl_id IN (SELECT id FROM product_template WHERE categ_id NOT IN ({cat_list}));")
            # Hapus template produk diluar kategori kemuning
            self.env.cr.execute(f"DELETE FROM product_template WHERE categ_id NOT IN ({cat_list});")
            # Hapus kategori produk lain yang bukan milik kemuning dan bukan root (parent_id is not null)
            self.env.cr.execute(f"DELETE FROM product_category WHERE id NOT IN ({cat_list}) AND parent_id IS NOT NULL;")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Pembersihan Sukses',
                'message': 'Semua data demo bawaan Odoo (Meja, Kursi, dll) telah dihapus secara bersih!',
                'type': 'success',
                'sticky': False,
            }
        }
