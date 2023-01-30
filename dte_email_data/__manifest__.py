# -*- coding: utf-8 -*-
{
    'name': 'DTE CMCorp',
    'version': '2.0',
    'author': "CMCorp",
    'summary': """
        Setea automaticamente en correo DTE de empresa
    """,
    'sequence': -100,
    'description': """
        Al ingresar el Rut de la empresa, se une automaticamente el correo a la empresa.
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'contacts',
        'l10n_cl_edi',
    ],
    'data':  [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/dte_partner.xml',
        'views/synchro_partner.xml',
        'views/message.xml',
        'views/partner.xml',
        'views/certificate.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}