# -*- coding: utf-8 -*-
{
    'name': 'Cambios productos AMSP ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Modificación de productos para AMSP

    """,
    'sequence': -100,
    'description': """
       Modificación de productos y adhisión a valores nuevos  para AMSP
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'sale_management',
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/ir_ui_view.xml',
        'views/product.xml',
        'views/product_tonnage.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}