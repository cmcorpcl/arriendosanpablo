# -*- coding: utf-8 -*-
{
    'name': 'Delivery Guide (52 CL) Massive On Batch',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Creación de guias de despacho (CL) masivas en agrupación de albaranes
    """,
    'sequence': -100,
    'description': """
        Creación de botones para crear e imprimir guias de despacho (52)
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'stock',
        'l10n_cl_edi',
        'l10n_cl_edi_stock',
        'stock_picking_batch'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/stock_picking_batch.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}