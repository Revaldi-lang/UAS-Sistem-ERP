# -*- coding: utf-8 -*-
from odoo import models, fields

class PosOrderReport(models.Model):
    _inherit = 'report.pos.order'

    is_imported = fields.Boolean(
        string="Bunga Impor?", 
        readonly=True,
        help="Status apakah bunga yang terjual melalui POS merupakan bunga impor."
    )

    def _select(self):
        res = super()._select()
        # pt adalah alias untuk product_template di report.pos.order
        res += ", pt.is_imported AS is_imported"
        return res

    def _group_by(self):
        res = super()._group_by()
        # Harus memasukkan kolom pt.is_imported ke GROUP BY untuk mencegah database view error
        res += ", pt.is_imported"
        return res
