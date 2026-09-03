# -*- coding: utf-8 -*-
from odoo import models, fields, tools


class MbaBiPurchaseTransit(models.Model):
    _name = "mba.bi.purchase.transit"
    _description = "BI - Análisis de Compras en Tránsito por Día"
    _auto = False
    _order = "date_planned asc, transit_value desc"

    order_id = fields.Many2one("purchase.order", string="Orden de Compra", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Proveedor", readonly=True)
    product_id = fields.Many2one("product.product", string="Producto", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", string="Plantilla de Producto", readonly=True)
    categ_id = fields.Many2one("product.category", string="Categoría", readonly=True)
    company_id = fields.Many2one("res.company", string="Compañía", readonly=True)
    date_order = fields.Datetime(string="Fecha de Orden", readonly=True)
    date_planned = fields.Datetime(string="Fecha Prevista de Recepción", readonly=True)
    date_planned_day = fields.Date(string="Día Previsto", readonly=True)
    product_qty = fields.Float(string="Cantidad Pedida", readonly=True)
    qty_received = fields.Float(string="Cantidad Recibida", readonly=True)
    qty_pending = fields.Float(string="Cantidad en Tránsito", readonly=True)
    price_unit = fields.Float(string="Precio Unitario", readonly=True)
    transit_value = fields.Float(string="Monto en Tránsito ($)", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    pol.id AS id,
                    pol.order_id AS order_id,
                    po.partner_id AS partner_id,
                    pol.product_id AS product_id,
                    pp.product_tmpl_id AS product_tmpl_id,
                    pt.categ_id AS categ_id,
                    pol.company_id AS company_id,
                    po.date_order AS date_order,
                    pol.date_planned AS date_planned,
                    pol.date_planned::date AS date_planned_day,
                    pol.product_qty AS product_qty,
                    pol.qty_received AS qty_received,
                    (pol.product_qty - COALESCE(pol.qty_received, 0.0)) AS qty_pending,
                    pol.price_unit AS price_unit,
                    (pol.product_qty - COALESCE(pol.qty_received, 0.0)) * pol.price_unit AS transit_value
                FROM purchase_order_line pol
                JOIN purchase_order po ON po.id = pol.order_id
                JOIN product_product pp ON pp.id = pol.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                WHERE po.state IN ('purchase', 'done')
                  AND (pol.product_qty - COALESCE(pol.qty_received, 0.0)) > 0
            )
        """)
