# -*- coding: utf-8 -*-
{
    'name': 'Actualizar multimoneda SBIF CMCORP ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
       Actualizar valores de  multimoneda por api SBIF CMCORP

    """,
    'sequence': -100,
    'description': """
        Actualizacion de valores de UF, USD, UTM, EUR a traves de la api de SBIF
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
    ],
    'data':  [
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}