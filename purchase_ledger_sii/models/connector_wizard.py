# -*- coding: utf-8 -*-

import json
from odoo import models, fields, api
import datetime
from requests import Session
from odoo.exceptions import UserError

MONTH_SELECTION =[
    ('01', 'Enero'),
    ('02', 'Febrero'),
    ('03', 'Marzo'),
    ('04', 'Abril'),
    ('05', 'Mayo'),
    ('06', 'Junio'),
    ('07', 'Julio'),
    ('08', 'Agosto'),
    ('09', 'Septiembre'),
    ('10', 'Octubre'),
    ('11', 'Noviembre'),
    ('12', 'Diciembre')]

def get_years():
    year_list = []
    count = 0
    now = datetime.datetime.now().year
    for i in range(2000, int(now)+1):
        year_list.append((str(i), str(i)))
        count += 1
    return year_list

class ConnectorWizard(models.TransientModel):
    _name = 'purchase_ledger.connector.wizard'
    _description = 'Elegir fecha y compañia para sincronizar libro de compra'

    company_id = fields.Many2one("res.company", string="Compañia", required=True )
    month = fields.Selection(MONTH_SELECTION, string="Mes")
    year = fields.Selection(get_years(), string="Año")
    #user_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user)

    def synchro_purchase_invoices(self):
        with Session() as s:
            if self.company_id.company_rut_sii and self.company_id.company_sii_pass:
                first_data = {
                    'rut': self.company_id.company_rut_sii[:-1].replace("-",""),
                    'dv':self.company_id.company_rut_sii[-1],
                    'referencia': 'https://misiir.sii.cl/cgi_misii/siihome.cgi',
                    'clave': self.company_id.company_sii_pass
                }
                first_headers = {'Content-type': 'application/x-www-form-urlencoded'}
                r = s.post("https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi", data=first_data, headers=first_headers)
                token = s.cookies.get("TOKEN")
                if token and r.status_code == 200:
                    second_headers = {'Content-type': 'application/json;charset=utf-8'}
                    second_data_info = {
                                    "metaData": {
                                        "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen",
                                        "conversationId": token,
                                        "transactionId": "1",
                                        "page": None
                                    },
                                    "data": {
                                        "rutEmisor": self.company_id.company_rut_sii[:-1].replace("-",""),
                                        "dvEmisor": self.company_id.company_rut_sii[-1],
                                        "ptributario": self.year+self.month,
                                        "estadoContab": "REGISTRO",
                                        "operacion": "COMPRA",
                                        "busquedaInicial": True
                                    }
                                    }
                    second_data = json.dumps(second_data_info)
                    r2 = s.post("https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen", data=second_data, headers=second_headers)
                    if r2.status_code == 200:
                        response_data2 = json.loads(r2.text)
                        if response_data2['data'] is not None:
                            for doct in response_data2['data']:
                                third_headers = {'Content-type': 'application/json;charset=utf-8'}
                                third_data_info = {
                                    'data': {
                                                "rutEmisor": self.company_id.company_rut_sii[:-1].replace("-",""),
                                                "dvEmisor": self.company_id.company_rut_sii[-1],
                                                "ptributario": self.year+self.month,
                                                "codTipoDoc": doct['rsmnTipoDocInteger'],
                                                "operacion": "COMPRA",
                                                "estadoContab": "REGISTRO"
                                            },
                                        "metaData": {
                                                    "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleCompra",
                                                    "conversationId": token,
                                                    "transactionId": "1",
                                                    "page": None
                                                    },
                                }
                                third_data = json.dumps(third_data_info)
                                r3 = s.post("https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleCompra", data=third_data, headers=third_headers)
                                if r3.status_code == 200:
                                    response_data3 = json.loads(r3.text)
                                    for file in response_data3['data']:
                                        ledger_invoice_env = self.env['purchase.ledger.invoice']
                                        ledger_invoice_encounter = ledger_invoice_env.search([('invoice_number', '=', file['detNroDoc']), ('bussiness_line', '=', file['detRznSoc'])])
                                        if len(ledger_invoice_encounter) < 1:
                                            rut = str(file['detRutDoc']) + '-' + str(file['detDvDoc'])
                                            ledger_invoice_data = {
                                                'invoice_number': str(file['detNroDoc']),
                                                'bussiness_line': file['detRznSoc'],
                                                'invoice_rut': rut,
                                                'invoice_type': '(' + str(doct['rsmnTipoDocInteger']) + ') ' + doct['dcvNombreTipoDoc'],
                                                'invoice_type_code': str(doct['rsmnTipoDocInteger']),
                                                'date' : datetime.datetime.strptime(file['detFchDoc'] , '%d/%m/%Y').date(),
                                                'net_amount': file['detMntNeto'],
                                                'tax_amount': file['detMntIVA'],
                                                'exnt_amount': file['detMntExe'],
                                                'total_amount': file['detMntTotal'],
                                                'state': '3',
                                                'currency_id': 45,
                                                'company_id': self.company_id.id
                                            }
                                            partner_encounter = self.env['res.partner'].search([('vat','=', rut)])
                                            if len(partner_encounter) > 0:
                                                ledger_invoice_data['partner_id'] = partner_encounter[0].id
                                            invoice_encounter = self.env['account.move'].search([('sequence_number','ilike', file['detNroDoc']), ('partner_id.vat','=', rut)])
                                            if len(invoice_encounter) > 0:
                                                ledger_invoice_data['invoice_id'] = invoice_encounter[0].id
                                                if invoice_encounter[0].amount_total != file['detMntTotal']:
                                                    ledger_invoice_data['state'] = '2'
                                                else:
                                                    ledger_invoice_data['state'] = '1'
                                            ledger_values  = ledger_invoice_env.create(ledger_invoice_data)
                                            if len(invoice_encounter) > 0:
                                                invoice_encounter[0].write({'invoice_ledger_id': ledger_values.id})
                                else:
                                    raise UserError("No se ha conseguido conectar con los documentos del libro de compras, revise su señal de internet e intente denuevo.")
                        else:
                            raise UserError("El libro de compra no presenta documentos para su sincronización.")
                    else:
                        raise UserError("No se ha conseguido conectar con el libro de compras, revise su señal de internet e intente denuevo.")
                else:
                    raise UserError("No se ha podido ingresar a SII, revise el rut y la contraseña de la compañia para su ingreso.")
            else:
                raise UserError("La compañia no presenta los datos de autentificación para buscar su libro de compra.")
        return  {
            'name': 'Libro de compra',
            'view_mode':'tree,form',
            'view_type':'form',
            'res_model':'purchase.ledger.invoice',
            'views': [(self.env.ref('purchase_ledger_sii.purchase_ledger_tree').id, 'tree'),
                      (self.env.ref('purchase_ledger_sii.purchase_ledger_form').id, 'form')],
            'type':'ir.actions.act_window',
            'target': 'main',
            'nodestroy': True
        }


    def _cron_ledger(self):
        month = str(datetime.datetime.now().month)
        if len(month) < 2:
            month = "0" + month
        year = str(datetime.datetime.now().year)
        date = str(year) + str(month)
        company_encounter = self.env['res.company'].search([])
        for company in company_encounter:
            if company.company_rut_sii  and company.company_sii_pass:
                with Session() as s:
                    first_data = {
                        'rut': company.company_rut_sii[:-1].replace("-",""),
                        'dv':company.company_rut_sii[-1],
                        'referencia': 'https://misiir.sii.cl/cgi_misii/siihome.cgi',
                        'clave': company.company_sii_pass
                    }
                    first_headers = {'Content-type': 'application/x-www-form-urlencoded'}
                    r = s.post("https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi", data=first_data, headers=first_headers)
                    token = s.cookies.get("TOKEN")
                    if token and r.status_code == 200:
                        second_headers = {'Content-type': 'application/json;charset=utf-8'}
                        second_data_info = {
                                        "metaData": {
                                            "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen",
                                            "conversationId": token,
                                            "transactionId": "1",
                                            "page": None
                                        },
                                        "data": {
                                            "rutEmisor": company.company_rut_sii[:-1].replace("-",""),
                                            "dvEmisor": company.company_rut_sii[-1],
                                            "ptributario": date,
                                            "estadoContab": "REGISTRO",
                                            "operacion": "COMPRA",
                                            "busquedaInicial": True
                                        }
                                        }
                        second_data = json.dumps(second_data_info)
                        r2 = s.post("https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen", data=second_data, headers=second_headers)
                        if r2.status_code == 200:
                            response_data2 = json.loads(r2.text)
                            if response_data2['data'] is not None:
                                for doct in response_data2['data']:
                                    third_headers = {'Content-type': 'application/json;charset=utf-8'}
                                    third_data_info = {
                                        'data': {
                                                    "rutEmisor": company.company_rut_sii[:-1].replace("-",""),
                                                    "dvEmisor": company.company_rut_sii[-1],
                                                    "ptributario": date,
                                                    "codTipoDoc": doct['rsmnTipoDocInteger'],
                                                    "operacion": "COMPRA",
                                                    "estadoContab": "REGISTRO"
                                                },
                                            "metaData": {
                                                        "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleCompra",
                                                        "conversationId": token,
                                                        "transactionId": "1",
                                                        "page": None
                                                        },
                                    }
                                    third_data = json.dumps(third_data_info)
                                    r3 = s.post("https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleCompra", data=third_data, headers=third_headers)
                                    if r3.status_code == 200:
                                        response_data3 = json.loads(r3.text)
                                        for file in response_data3['data']:
                                            ledger_invoice_env = self.env['purchase.ledger.invoice']
                                            ledger_invoice_encounter = ledger_invoice_env.search([('invoice_number', '=', file['detNroDoc']), ('bussiness_line', '=', file['detRznSoc'])])
                                            if len(ledger_invoice_encounter) < 1:
                                                rut = str(file['detRutDoc']) + '-' + str(file['detDvDoc'])
                                                ledger_invoice_data = {
                                                    'invoice_number': str(file['detNroDoc']),
                                                    'bussiness_line': file['detRznSoc'],
                                                    'invoice_rut': rut,
                                                    'invoice_type': '(' + str(doct['rsmnTipoDocInteger']) + ') ' + doct['dcvNombreTipoDoc'],
                                                    'invoice_type_code': str(doct['rsmnTipoDocInteger']),
                                                    'date' : datetime.datetime.strptime(file['detFchDoc'] , '%d/%m/%Y').date(),
                                                    'net_amount': file['detMntNeto'],
                                                    'tax_amount': file['detMntIVA'],
                                                    'exnt_amount': file['detMntExe'],
                                                    'total_amount': file['detMntTotal'],
                                                    'state': '3',
                                                    'currency_id': 45,
                                                    'company_id': company.id
                                                }
                                                partner_encounter = self.env['res.partner'].search([('vat','=', rut)])
                                                if len(partner_encounter) > 0:
                                                    ledger_invoice_data['partner_id'] = partner_encounter[0].id
                                                invoice_encounter = self.env['account.move'].search([('sequence_number','ilike', file['detNroDoc']), ('partner_id.vat','=', rut)])
                                                if len(invoice_encounter) > 0:
                                                    ledger_invoice_data['invoice_id'] = invoice_encounter[0].id
                                                    if invoice_encounter[0].amount_total != file['detMntTotal']:
                                                        ledger_invoice_data['state'] = '2'
                                                    else:
                                                        ledger_invoice_data['state'] = '1'
                                                ledger_values  = ledger_invoice_env.create(ledger_invoice_data)
                                                if len(invoice_encounter) > 0:
                                                    invoice_encounter[0].write({'invoice_ledger_id': ledger_values.id})