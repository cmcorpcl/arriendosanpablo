
import datetime
from http import server
from lxml import etree
from dateutil.relativedelta import relativedelta
import re
import logging
from pytz import timezone

import requests

from odoo import api, fields, models
from odoo.addons.web.controllers.main import xml2json_from_elementtree
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

BANXICO_DATE_FORMAT = '%d/%m/%Y'
CBUAE_URL = "https://www.centralbank.ae/en/fx-rates"
CBUAE_CURRENCIES = {
    'US Dollar': 'USD',
    'Argentine Peso': 'ARS',
    'Australian Dollar': 'AUD',
    'Bangladesh Taka': 'BDT',
    'Bahrani Dinar': 'BHD',
    'Brunei Dollar': 'BND',
    'Brazilian Real': 'BRL',
    'Botswana Pula': 'BWP',
    'Belarus Rouble': 'BYN',
    'Canadian Dollar': 'CAD',
    'Swiss Franc': 'CHF',
    'Chilean Peso': 'CLP',
    'Chinese Yuan - Offshore': 'CNY',
    'Chinese Yuan': 'CNY',
    'Colombian Peso': 'COP',
    'Czech Koruna': 'CZK',
    'Danish Krone': 'DKK',
    'Algerian Dinar': 'DZD',
    'Egypt Pound': 'EGP',
    'Euro': 'EUR',
    'GB Pound': 'GBP',
    'Hongkong Dollar': 'HKD',
    'Hungarian Forint': 'HUF',
    'Indonesia Rupiah': 'IDR',
    'Indian Rupee': 'INR',
    'Iceland Krona': 'ISK',
    'Jordan Dinar': 'JOD',
    'Japanese Yen': 'JPY',
    'Kenya Shilling': 'KES',
    'Korean Won': 'KRW',
    'Kuwaiti Dinar': 'KWD',
    'Kazakhstan Tenge': 'KZT',
    'Lebanon Pound': 'LBP',
    'Sri Lanka Rupee': 'LKR',
    'Moroccan Dirham': 'MAD',
    'Macedonia Denar': 'MKD',
    'Mexican Peso': 'MXN',
    'Malaysia Ringgit': 'MYR',
    'Nigerian Naira': 'NGN',
    'Norwegian Krone': 'NOK',
    'NewZealand Dollar': 'NZD',
    'Omani Rial': 'OMR',
    'Peru Sol': 'PEN',
    'Philippine Piso': 'PHP',
    'Pakistan Rupee': 'PKR',
    'Polish Zloty': 'PLN',
    'Qatari Riyal': 'QAR',
    'Serbian Dinar': 'RSD',
    'Russia Rouble': 'RUB',
    'Saudi Riyal': 'SAR',
    'Swedish Krona': 'SWK',
    'Singapore Dollar': 'SGD',
    'Thai Baht': 'THB',
    'Tunisian Dinar': 'TND',
    'Turkish Lira': 'TRY',
    'Trin Tob Dollar': 'TTD',
    'Taiwan Dollar': 'TWD',
    'Tanzania Shilling': 'TZS',
    'Uganda Shilling': 'UGX',
    'Vietnam Dong': 'VND',
    'South Africa Rand': 'ZAR',
    'Zambian Kwacha': 'ZMW',
}

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    currency_provider = fields.Selection([
        ('ecb', 'European Central Bank'),
        ('fta', 'Federal Tax Administration (Switzerland)'),
        ('banxico', 'Mexican Bank'),
        ('boc', 'Bank Of Canada'),
        ('xe_com', 'xe.com'),
        ('bnr', 'National Bank Of Romania'),
        ('mindicador', 'Chilean mindicador.cl'),
        ('sbif','Chilean Sbif'),
        ('bcrp', 'Bank of Peru'),
        ('cbuae', 'UAE Central Bank'),
    ], default='ecb', string='Service Provider')


    def _parse_sbif_data(self, available_currencies):
        """Parse function for mindicador.cl provider for Chile
        * Regarding needs of rates in Chile there will be one rate per day, except for UTM index (one per month)
        * The value of the rate is the "official" rate
        * The base currency is always CLP but with the inverse 1/rate.
        * The webservice returns the following currency rates:
            - EUR
            - USD (Dolar Observado)
            - UF (Unidad de Fomento)
            - UTM (Unidad Tributaria Mensual)
        """
        icp = self.env['ir.config_parameter'].sudo()
        server_url = icp.get_param('sbif_api_url', False)
        apikey = icp.get_param("sbif_financial_indicators_apikey")
        if not server_url:
            server_url = 'https://api.cmfchile.cl/api-sbifv3/recursos_api'
            icp.set_param('sbif_api_url', server_url)
        foreigns = {
            "USD": ["dolar", "Dolares"],
            "EUR": ["euro", "Euros"],
            "UF": ["uf", "UFs"],
            "UTM": ["utm", "UTMs"],
        }
        available_currency_names = available_currencies.mapped('name')
        _logger.debug('sbif: available currency names: %s' % available_currency_names)
        today_date = fields.Date.context_today(self.with_context(tz='America/Santiago'))
        rslt = {
            'CLP': (1.0, today_date.strftime(DEFAULT_SERVER_DATE_FORMAT)),
        }
        request_date = today_date.strftime('%d-%m-%Y')
        for index, currency in foreigns.items():
            if index not in available_currency_names:
                _logger.debug('Index %s not in available currency name' % index)
                continue
            url = "%s/%s?apikey=%s&formato=json" % (server_url, currency[0], apikey)
            try:
                res = requests.get(url)
                res.raise_for_status()
            except Exception as e:
                return False
            if 'html' in res.text:
                return False
            data_json = res.json()
            if len(data_json[currency[1]]) == 0:
                continue
            date = data_json[currency[1]][0]['Fecha'][:10]
            value = data_json[currency[1]][0]['Valor']
            valor = value.replace('.','').replace(",", ".")
            rate = float(valor)
            rslt[index] = (1.0 / rate,  date)
        print(rslt)
        return rslt
