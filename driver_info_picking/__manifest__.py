# -*- coding: utf-8 -*-
{
    'name': 'Driver Info Picking for Delivery Guide(52)',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Información de conductor en Guia de despacho (52) Chile
    """,
    'sequence': -100,
    'description': """
        Se agregan 4 campos a la guia de despacho siendo estos conductor, patente, rut de conductor y dirección de entrega
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'hr',
        'stock',
        'l10n_cl_edi_stock',
        'sale',
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/partner.xml',
        'views/sale_order.xml',
        'views/report_guide_dte52.xml',
        'views/stock_picking_batch.xml',
        'views/guide_truck.xml',
        'views/destination_zone.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}