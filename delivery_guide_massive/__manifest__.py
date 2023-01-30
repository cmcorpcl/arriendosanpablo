# -*- coding: utf-8 -*-
{
    'name': 'Delivery Guide (52 CL) Massive Creation CheckMate',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Creación de guias de despacho (CL) masivas
    """,
    'sequence': -100,
    'description': """
        Creación de boton en inventario para la creación masiva de guias de despacho
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'contacts',
        'l10n_cl_edi',
        'l10n_cl_edi_stock'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/stock_picking.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}