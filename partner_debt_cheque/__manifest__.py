# -*- coding: utf-8 -*-
{
    'name': 'Partner Debt With Cheque ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Ingresar cheques a deuda de contacto

    """,
    'sequence': -100,
    'description': """
        Se ingresaran las lineas de cheques no cobrados en las deudas del contacto
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'contacts',
        'account_followup'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/res_partner.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}