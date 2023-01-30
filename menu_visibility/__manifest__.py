# -*- coding: utf-8 -*-
{
    'name': 'Menu visibility CMCorp ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Visibilizar menu para ciertos usuarios

    """,
    'sequence': -100,
    'description': """
         Visibilizar ciertos menu para ciertos usuarios y dejar invisible para los demas
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'contacts',
        'hr',
    ],
    'data':  [
        'security/ir.model.access.csv',
        'security/security.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}