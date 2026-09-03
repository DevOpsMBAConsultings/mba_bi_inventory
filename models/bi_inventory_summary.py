# -*- coding: utf-8 -*-
from odoo import models, fields, tools


class MbaBiInventorySummary(models.Model):
    _name = "mba.bi.inventory.summary"
    _description = "BI - Resumen de Inventario Operativo y Stock Físico"
    _auto = False

    product_id = fields.Many2one("product.product", string="Producto", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", string="Plantilla de Producto", readonly=True)
    categ_id = fields.Many2one("product.category", string="Categoría", readonly=True)
    location_id = fields.Many2one("stock.location", string="Ubicación Interna", readonly=True)
    company_id = fields.Many2one("res.company", string="Compañía", readonly=True)
    physical_qty = fields.Float(string="Stock Físico (>0)", readonly=True)
    cost = fields.Float(string="Costo Unitario", readonly=True)
    physical_value = fields.Float(string="Valor Físico en Bodega ($)", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    sq.id AS id,
                    sq.product_id AS product_id,
                    pp.product_tmpl_id AS product_tmpl_id,
                    pt.categ_id AS categ_id,
                    sq.location_id AS location_id,
                    sq.company_id AS company_id,
                    sq.quantity AS physical_qty,
                    COALESCE((pp.standard_price->>sq.company_id::text)::numeric, (pp.standard_price->>'1')::numeric, 0.0) AS cost,
                    sq.quantity * COALESCE((pp.standard_price->>sq.company_id::text)::numeric, (pp.standard_price->>'1')::numeric, 0.0) AS physical_value
                FROM stock_quant sq
                JOIN stock_location sl ON sl.id = sq.location_id
                JOIN product_product pp ON pp.id = sq.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                WHERE sl.usage = 'internal'
                  AND sq.quantity > 0
            )
        """)
