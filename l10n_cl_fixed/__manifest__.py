# -*- coding: utf-8 -*-
{
    'name': "Arreglar Modulo l10n_cl general",

    'summary': """
        Arreglos para el modulo de facturación y despacho de chile""",

    'description': """
        Arreglos para el modulo de facturación y despacho de chile como el tamaño de letra de factura, fechas, etc.
    """,

    'author': "CMCorp",
    'website': "http://consulnet.cl",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_cl_edi','account','account_debit_note',
        'l10n_cl',],

    # always loaded
    'data': [
        'views/report_picking.xml',
        'views/report_account.xml',
        'views/partner.xml'
        # 'template/templates.xml',
        # 'template/template_signature.xml',
        # 'views/account_move_views.xml'
    ],
}