# -*- coding: utf-8 -*-
{
    'name': 'Factura con guias de despacho ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Factura con de guías de despacho en referencias cruzadas

    """,
    'sequence': -100,
    'description': """
        Creación de facturas con guias de despacho en referencias cruzadas
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'sale_management',
        'stock',
        'l10n_cl_edi_stock',
        'l10n_cl_edi',
        'l10n_cl',
        'account_accountant'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'views/stock_picking.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}