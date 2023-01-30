# -*- coding: utf-8 -*-
{
    'name': 'Purchase Ledger connector to SII',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Conector del libro de compras de SII
    """,
    'sequence': -100,
    'description': """
        Conector directo con el libro de compras de la compañia en el SII
    """,
    'category': '',
    'website': 'https://www.checkmateagencia.cl',
    'depends':  [
        'l10n_latam_invoice_document',

    ],
    'data':  [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/company.xml',
        'views/purchase_ledger.xml',
        'views/connector.xml',
        'views/create_invoice.xml',
        'views/account_move.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}