# -*- coding: utf-8 -*-
{
    'name': 'Sale order and invoice connector',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Conector de pedidos con facturas
    """,
    'sequence': -100,
    'description': """
        Permite conectar una factura con un pedido creado del mismo cliente
    """,
    'category': '',
    'website': 'https://www.checkmateagencia.cl',
    'depends':  [
        'contacts',
        'purchase',
        'sale_management'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/account_move.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}