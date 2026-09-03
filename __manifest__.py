# -*- coding: utf-8 -*-
{
    "name": "BI Inventario y Abastecimiento Operativo (MBA Consultings)",
    "version": "18.0.1.0.0",
    "category": "Inventory/Analytics",
    "summary": "Tablero ejecutivo y analítica de inventario: Stock físico, déficit por ventas negativas y compras en tránsito | MBA Consultings",
    "description": """
BI Inventario y Abastecimiento Operativo
=========================================

Add-on satélite para **mba_bi_dashboard** que despliega de forma automática un cuadro de mando
gerencial para el control de inventarios, abastecimiento y proyección operativa:

Características Principales:
-----------------------------
* **Físico en Bodega (Stock > 0)**: Valorización en tiempo real del inventario real positivo en ubicaciones internas.
* **Déficit por Ventas Negativas**: Monitoreo y alerta inmediata de existencias bajo cero generadas por ventas/despachos sin entrada previa.
* **Compras en Tránsito**: Órdenes de compra confirmadas pendientes de recepción valorizadas a precio pactado.
* **Inventario Operativo Proyectado**: Balance neto real (Físico - Déficit + Tránsito).
* **Detalle Día a Día**:
  - Gráficos y listas de compras en camino por fecha prevista de recepción (`date_planned`).
  - Lista detallada de productos con déficit negativo para auditoría inmediata.
* **Cero Configuración**: Al instalarse, crea automáticamente el tablero, KPIs y vistas en el menú de BI.
    """,
    "author": "MBA Consultings, Brooks Gonzalez",
    "website": "https://mbaconsultings.com",
    "license": "LGPL-3",
    "depends": [
        "mba_bi_dashboard",
        "stock",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/bi_inventory_views.xml",
        "data/dashboard_inventory_data.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
