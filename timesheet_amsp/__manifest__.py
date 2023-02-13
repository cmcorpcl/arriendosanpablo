# -*- coding: utf-8 -*-
{
    'name': 'Numero de reporte y horometro en parte por hora ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
Numero de reporte y horometro en parte por hora

    """,
    'sequence': -100,
    'description': """
Numero de reporte y horometro en parte por hora
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'hr_timesheet',
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/account_analytic_line.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}