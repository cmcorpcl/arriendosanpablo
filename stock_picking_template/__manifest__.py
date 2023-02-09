# -*- coding: utf-8 -*-
{
    'name': 'Stock picking template',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Preconfigured templates for stock picking

    """,
    'sequence': -100,
    'description': """
        Preconfigured templates for stock picking
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'stock',
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