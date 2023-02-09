# -*- coding: utf-8 -*-
{
    'name': 'Change company in sale order/ rental ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Cambia la compañia de los pedidos a otra compañia junto a sus lineas que presentan tareas dentro

    """,
    'sequence': -100,
    'description': """
        Cambia la compañia de los pedidos a otra compañia junto a sus lineas que presentan tareas dentro
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'sale_management',
        'sale_stock'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/change_sale_company.xml',
        'views/project.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}