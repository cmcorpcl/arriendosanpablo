# -*- coding: utf-8 -*-
{
    'name': 'Default days plus in sale order',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Se determinan dias para sumar a la fecha de las notas de ventas
    """,
    'sequence': -100,
    'description': """
        Se determinan dias para sumar a la fecha de las notas de ventas
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'sale_management',
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/res_config_settings.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}