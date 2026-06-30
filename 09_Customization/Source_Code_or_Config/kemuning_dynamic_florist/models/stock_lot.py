# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class StockLot(models.Model):
    _inherit = 'stock.lot'

    days_to_expire = fields.Integer(
        string="Hari Menuju Layu",
        compute="_compute_days_to_expire",
        help="Sisa hari sebelum bunga segar layu (berdasarkan Tanggal Kadaluwarsa)."
    )
    is_expired_soon = fields.Boolean(
        string="Hampir Layu?",
        compute="_compute_days_to_expire",
        help="Menandai jika umur bunga tinggal 24 jam atau kurang sebelum layu."
    )

    @api.depends('expiration_date')
    def _compute_days_to_expire(self):
        now = fields.Datetime.now()
        for lot in self:
            if lot.expiration_date:
                delta = lot.expiration_date - now
                seconds = delta.total_seconds()
                
                # Menghitung sisa hari
                if seconds > 0:
                    days = int(seconds / 86400)
                    lot.days_to_expire = days
                    # Jika sisa waktu <= 24 jam (86400 detik)
                    lot.is_expired_soon = (seconds <= 86400.0)
                else:
                    lot.days_to_expire = 0
                    lot.is_expired_soon = True
            else:
                # Nilai default jika lot tidak memiliki tanggal kadaluwarsa
                lot.days_to_expire = 999
                lot.is_expired_soon = False
