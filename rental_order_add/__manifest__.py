# -*- coding: utf-8 -*-
{
    'name': 'Adicionales alquiler A. San Pablo',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Valores adicionales para los formularios de arquiler en Arriendos San Pablo

    """,
    'sequence': -100,
    'description': """
        Valores adicionales para los formularios de arquiler en Arriendos San Pablo
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'sale_management',
        'sale_renting'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/hr_employee.xml',
        'views/sale_order.xml',
        'views/sale_order_report.xml',
        'views/account_move_report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}