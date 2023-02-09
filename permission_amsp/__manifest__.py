# -*- coding: utf-8 -*-
{
    'name': 'Permisos usuario AMSP ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Permisos de usuarios para arriendo san pablo

    """,
    'sequence': -100,
    'description': """
        Permisos de usuarios para arriendo san pablo
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'fleet_rental',
        'rental_order_add',
        'fleet_external_services'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/res_users.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}