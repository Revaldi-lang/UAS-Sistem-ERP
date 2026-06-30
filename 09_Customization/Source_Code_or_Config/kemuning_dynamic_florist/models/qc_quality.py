# -*- coding: utf-8 -*-
from odoo import models, fields, api

class QcQualityPoint(models.Model):
    _name = 'qc.quality.point'
    _description = 'Quality Control Point'

    name = fields.Char(string="Nama Pemeriksaan", required=True)
    category_id = fields.Many2one('qc.test.category', string="Kategori Uji")
    product_tmpl_id = fields.Many2one('product.template', string="Produk", domain=[('is_flower', '=', True)])
    instruction = fields.Text(string="Instruksi Pengujian")


class QcQualityCheck(models.Model):
    _name = 'qc.quality.check'
    _description = 'Quality Control Check'
    _order = 'id desc'

    name = fields.Char(string="Kode Inspeksi", required=True, default="QC-CHECK")
    point_id = fields.Many2one('qc.quality.point', string="Titik Kontrol", required=True)
    product_id = fields.Many2one('product.product', string="Produk Terkait", required=True)
    lot_id = fields.Many2one('stock.lot', string="Nomor Lot/Serial", domain="[('product_id', '=', product_id)]")
    state = fields.Selection([
        ('draft', 'Belum Diuji'),
        ('pass', 'Lolos Uji (Pass)'),
        ('fail', 'Gagal Uji (Fail)')
    ], string="Status Kelayakan", default='draft', required=True)
    notes = fields.Text(string="Catatan Inspeksi")
    date_checked = fields.Datetime(string="Tanggal Pemeriksaan", default=fields.Datetime.now)

    def action_pass(self):
        for record in self:
            record.state = 'pass'

    def action_fail(self):
        for record in self:
            record.state = 'fail'
