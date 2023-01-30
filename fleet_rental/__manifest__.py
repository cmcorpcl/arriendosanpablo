# -*- coding: utf-8 -*-
{
    'name': 'Flota y arriendo para AMSP ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Valores necesarios para flota y traspaso de dato en arriendo

    """,
    'sequence': -100,
    'description': """
        Valores necesarios para flota y traspaso de dato en arriendo
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'sale_renting',
        'fleet'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/fleet.xml',
        'views/fleet_situation_type.xml',
        'views/fleet_vehicule_license.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}