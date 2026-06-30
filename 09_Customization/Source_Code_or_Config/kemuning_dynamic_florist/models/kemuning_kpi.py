# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta

class KemuningKpi(models.Model):
    _name = 'kemuning.kpi'
    _description = 'Kemuning Florist KPI Dashboard'
    _order = 'sequence, id'

    name = fields.Char(string="Nama Indikator", required=True)
    value_text = fields.Char(string="Nilai", compute="_compute_kpi_value")
    value_num = fields.Float(string="Nilai Numerik", compute="_compute_kpi_value", store=True)
    category = fields.Selection([
        ('sales', 'Penjualan & Kasir'),
        ('inventory', 'Inventaris & Umur Bunga'),
        ('production', 'Produksi'),
        ('finance', 'Keuangan'),
    ], string="Kategori", default='sales')
    icon = fields.Char(string="Icon")
    sequence = fields.Integer(string="Urutan", default=10)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Paksa recompute semua record KPI sebelum dibaca untuk disajikan ke view/grafik
        self.search([])._compute_kpi_value()
        return super(KemuningKpi, self).search_read(domain, fields, offset, limit, order)

    def _compute_kpi_value(self):
        now = fields.Datetime.now()
        one_day_later = now + timedelta(days=1)
        for record in self:
            if record.name == "Total Variasi Bunga":
                count = self.env['product.template'].search_count([('is_flower', '=', True)])
                record.value_text = f"{count} Jenis Bunga"
                record.value_num = float(count)
                
            elif record.name == "Proporsi Bunga Impor":
                total = self.env['product.template'].search_count([('is_flower', '=', True)])
                imported = self.env['product.template'].search_count([('is_flower', '=', True), ('is_imported', '=', True)])
                pct = (imported / total * 100) if total > 0 else 0
                record.value_text = f"{imported} Impor dari {total} ({pct:.1f}%)"
                record.value_num = float(imported)
                
            elif record.name == "Bunga Hampir Layu (<= 24 Jam)":
                count = self.env['stock.lot'].search_count([
                    ('product_id.is_flower', '=', True),
                    ('expiration_date', '!=', False),
                    ('expiration_date', '<=', one_day_later)
                ])
                record.value_text = f"{count} Lot Bunga"
                record.value_num = float(count)
                
            elif record.name == "Total Penjualan Bunga":
                sales_lines = self.env['sale.order.line'].search([
                    ('product_id.is_flower', '=', True),
                    ('state', 'in', ['sale', 'done'])
                ])
                amount_sales = sum(sales_lines.mapped('price_subtotal'))
                
                pos_lines = self.env['pos.order.line'].search([
                    ('product_id.is_flower', '=', True)
                ])
                amount_pos = sum(pos_lines.mapped('price_subtotal'))
                
                total_amount = amount_sales + amount_pos
                record.value_text = f"Rp {total_amount:,.2f}"
                record.value_num = float(total_amount)
                
            else:
                record.value_text = "0"
                record.value_num = 0.0

    def action_refresh_kpi(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
