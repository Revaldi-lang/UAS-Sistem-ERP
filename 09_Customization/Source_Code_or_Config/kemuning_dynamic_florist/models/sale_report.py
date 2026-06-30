# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleReport(models.Model):
    _inherit = 'sale.report'

    is_imported = fields.Boolean(
        string="Bunga Impor?", 
        readonly=True,
        help="Status apakah bunga yang terjual merupakan bunga impor."
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        # t adalah alias untuk tabel product_template dalam query sale.report Odoo 17
        res['is_imported'] = "t.is_imported"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        # Harus memasukkan kolom t.is_imported ke GROUP BY untuk mencegah database view error
        res += ", t.is_imported"
        return res
