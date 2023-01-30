# -*- coding: utf-8 -*-
{
    'name': 'Union flota servicio externo AMSP ',
    'version': '1.0',
    'author': "CMCorp",
    'summary': """
        Union flota servicio externo AMSP

    """,
    'sequence': -100,
    'description': """
        Union flota servicio externo AMSP
    """,
    'category': '',
    'website': 'https://www.cmcorp.cl',
    'depends':  [
        'fleet',
        'industry_fsm',
        'mail'
    ],
    'data':  [
        'security/ir.model.access.csv',
        'views/fleet_log_services.xml',
        'views/partner_category.xml',
        'views/fleet_service_notification.xml',
        'views/project.xml',
        'views/fleet_model.xml',
        'views/mail_channel.xml',
        'views/fleet_vehicle.xml',
        'views/project_task_type.xml',
        'views/stock_production_lot.xml',
        'views/sale_order.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}