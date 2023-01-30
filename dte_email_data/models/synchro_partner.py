import csv
from odoo import api, fields, models,_
from bs4 import BeautifulSoup
import base64
from odoo.exceptions import UserError
from requests_pkcs12 import get
from cryptography.fernet import Fernet



class SynchroPartnerWizard(models.TransientModel):
    _name = 'dte_email_data.synchro_partner.wizard'
    _description = 'Sincronizador de Listado DTE y contactos'


    def synchronization(self):
        certificate =  self.env['l10n_cl.certificate'].search([],limit=1)
        priority_certificate = self.env['l10n_cl.certificate'].search([('priority_dte','=',True)],limit=1)
        if len(priority_certificate) > 0:
            certificate = priority_certificate
        if len(certificate) > 0:
            cert_file = certificate.signature_key_file
            cert_pass = certificate.signature_pass_phrase
            r = get("https://palena.sii.cl/cvc_cgi/dte/ce_consulta_rut", pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
            cookies = r.cookies
            print(r.status_code)
            if r.status_code == 200:
                r2 = get("https://palena.sii.cl/cvc_cgi/dte/ce_empresas_dwnld",cookies=cookies,pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
                print(r2.status_code)
                if r2.status_code == 200:
                    self.clear_all_records()
                    wrapper = csv.DictReader(r2.text.strip().split('\n'), delimiter=";")
                    for record in wrapper:
                        dte_partner = {
                            'rut': record['RUT'],
                            'bussiness_line': record['RAZON SOCIAL'],
                            'resolution_number': record['NUMERO RESOLUCION'],
                            'resolution_date': record['FECHA RESOLUCION'],
                            'dte_email':record['MAIL INTERCAMBIO'],
                            'url': record['URL']
                        }
                        dte_partner_env = self.env['dte_email_data.dte_partner']
                        values_dte_partner = dte_partner_env.create(dte_partner)
                    return  {
                        'name': 'Mensaje',
                        'view_mode':'form',
                        'view_type':'form',
                        'res_model':'dte_email_data.message.wizard',
                        'views': [(self.env.ref('dte_email_data.message_generator_dte_partner_wizard').id, 'form')],
                        'type':'ir.actions.act_window',
                        'target': 'new',
                    }
                else:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': _('Warning'),
                            'message':  'No se ha logrado obtener los datos de SII, intente mas tarde.',
                            'type': 'danger',  #types: success,warning,danger,info
                            'sticky': False,
                        }
                    }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Warning'),
                        'message':  'No se ha logrado la conexión con el SII, intente mas tarde.',
                        'type': 'danger',  #types: success,warning,danger,info
                        'sticky': False,
                    }
                }
        else:
            raise UserError('No presenta un certificado para poder hacer la comunicación con el SII')


    def clear_all_records(self):
        dte_partner_env = self.env['dte_email_data.dte_partner']
        all_dte_partner = dte_partner_env.search([])
        all_dte_partner.unlink()

    def synchro_with_res_partner(self):
        partner_env = self.env['res.partner']
        all_partner = partner_env.search([])
        flag = self.env.user.has_group('base.group_system')
        list_name = []
        list_name_no_rut = []
        cert_file = False
        cert_pass = False
        certificate =  self.env['l10n_cl.certificate'].search([],limit=1)
        priority_certificate = self.env['l10n_cl.certificate'].search([('priority_dte','=',True)],limit=1)
        if len(priority_certificate) > 0:
            certificate = priority_certificate
        if len(certificate) > 0:
            if certificate.signature_key_file:
                cert_file = certificate.signature_key_file
            if certificate.encrypt_pass:
                encrypt_pass = certificate.encrypt_pass
                key_st = certificate.key_encrypt + "546"
                key = key_st.encode()
                fernet = Fernet(key)
                cert_pass = fernet.decrypt((certificate.encrypt_pass).encode()).decode()
        else:
            raise UserError('No presenta un certificado para poder hacer la comunicación con el SII')
        if cert_file and cert_pass:
            r = get("https://palena.sii.cl/cvc_cgi/dte/ce_consulta_rut", pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
            cookies = r.cookies
            for partner in all_partner:
                dte_partner_env = self.env['dte_email_data.dte_partner']
                vat = partner.vat
                if vat:
                    vat = vat.replace(".",'')
                    vat = vat.replace(" " ,"")
                    vat = vat.upper()
                    if vat[0] == '0':
                        vat = vat[1:]
                    dte_partner_encounter = dte_partner_env.search([('rut','=', vat)])
                    if(len(dte_partner_encounter) > 0):
                        dte_partner = dte_partner_encounter[0]
                        partner.write({'l10n_cl_dte_email': dte_partner.dte_email,'name':dte_partner.bussiness_line})
                    else:
                        if r.status_code == 200:
                            print(vat)
                            params = {
                                "RUT_EMP": vat[:-1].replace("-",""),
                                "DV_EMP": vat[-1],
                                "ACEPTAR": "Consultar"
                            }
                            r2 = get("https://palena.sii.cl/cvc_cgi/dte/ce_consulta_e",cookies=cookies,params=params,pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
                            print(r2.text)
                            soup = BeautifulSoup(r2.text, 'html.parser')
                            tables =soup.find_all("table")
                            info = {

                            }
                            if len(tables) > 2:
                                rows = tables[2].find_all("tr")
                                for row in rows:
                                    td = row.find_all("td")
                                    td_label = td[0]
                                    td_target = td[1]
                                    label = td_label.find_all(text=True)
                                    text= td_target.find_all(text=True)
                                    texto= text[0]
                                    label_text = label[0]
                                    label_text = label_text.replace("\n","")
                                    label_text = label_text.replace("\xa0","")
                                    label_text = label_text.strip()
                                    texto = texto.replace("\n","")
                                    texto = texto.replace("\xa0","")
                                    texto = texto.strip()
                                    info[label_text] = texto
                            print(info)
                            if 'Mail de contacto' in info:
                                partner.write({'l10n_cl_dte_email': info['Mail de contacto'],'name':info['Razón Social/Nombres']})
                            else:
                                list_name.append(partner.name)
                        else:
                            list_name.append(partner.name)
                else:
                    list_name_no_rut.append(partner.name)
        else:
            raise UserError('Revisar certificado de SII')
        message_no_rut = ".\n".join(list_name_no_rut)
        message =  ".\n".join(list_name)
        return  {
            'name': 'Mensaje',
            'view_mode':'form',
            'view_type':'form',
            'res_model':'dte_email_data.message.wizard',
            'views': [(self.env.ref('dte_email_data.message_generator_wizard').id, 'form')],
            'context': {'default_message': message, 'default_message_no_rut': message_no_rut },
            'type':'ir.actions.act_window',
            'target': 'new',
                }

    def synchronization_cron(self):
        certificate =  self.env['l10n_cl.certificate'].search([],limit=1)
        priority_certificate = self.env['l10n_cl.certificate'].search([('priority_dte','=',True)],limit=1)
        if len(priority_certificate) > 0:
            certificate = priority_certificate
        if len(certificate) > 0:
            cert_file = certificate.signature_key_file
            cert_pass = certificate.signature_pass_phrase
            r = get("https://palena.sii.cl/cvc_cgi/dte/ce_consulta_rut", pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
            cookies = r.cookies
            if r.status_code == 200:
                r2 = get("https://palena.sii.cl/cvc_cgi/dte/ce_empresas_dwnld",cookies=cookies,pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
                if r2.status_code == 200:
                    self.clear_all_records()
                    wrapper = csv.DictReader(r2.text.strip().split('\n'), delimiter=";")
                    for record in wrapper:
                        dte_partner = {
                            'rut': record['RUT'],
                            'bussiness_line': record['RAZON SOCIAL'],
                            'resolution_number': record['NUMERO RESOLUCION'],
                            'resolution_date': record['FECHA RESOLUCION'],
                            'dte_email':record['MAIL INTERCAMBIO'],
                            'url': record['URL']
                        }
                        dte_partner_env = self.env['dte_email_data.dte_partner']
                        values_dte_partner = dte_partner_env.create(dte_partner)


    def synchro_with_res_partner_cron(self):
        partner_env = self.env['res.partner']
        all_partner = partner_env.search([])
        certificate =  self.env['l10n_cl.certificate'].search([],limit=1)
        priority_certificate = self.env['l10n_cl.certificate'].search([('priority_dte','=',True)],limit=1)
        if len(priority_certificate) > 0:
            certificate = priority_certificate
        if len(certificate) > 0:
            cert_file = certificate.signature_key_file
            cert_pass = certificate.signature_pass_phrase
            r = get("https://palena.sii.cl/cvc_cgi/dte/ce_consulta_rut", pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
            cookies = r.cookies
            for partner in all_partner:
                dte_partner_env = self.env['dte_email_data.dte_partner']
                vat = partner.vat
                if vat:
                    vat = vat.replace(".",'')
                    vat = vat.replace(" " ,"")
                    vat = vat.upper()
                    if vat[0] == '0':
                        vat = vat[1:]
                    dte_partner_encounter = dte_partner_env.search([('rut','=', vat)], limit=1)
                    if(len(dte_partner_encounter) > 0):
                        dte_partner = dte_partner_encounter[0]
                        partner.write({'l10n_cl_dte_email': dte_partner.dte_email,'name':dte_partner.bussiness_line})
                    else:
                        if r.status_code == 200:
                            params = {
                                "RUT_EMP": vat[:-1].replace("-",""),
                                "DV_EMP": vat[-1],
                                "ACEPTAR": "Consultar"
                            }
                            r2 = get("https://palena.sii.cl/cvc_cgi/dte/ce_consulta_e",cookies=cookies,params=params,pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
                            soup = BeautifulSoup(r2.text, 'html.parser')
                            tables =soup.find_all("table")
                            info = {}
                            if len(tables) > 2:
                                rows = tables[2].find_all("tr")
                                for row in rows:
                                    td = row.find_all("td")
                                    td_label = td[0]
                                    td_target = td[1]
                                    label = td_label.find_all(text=True)
                                    text= td_target.find_all(text=True)
                                    texto= text[0]
                                    label_text = label[0]
                                    label_text = label_text.replace("\n","")
                                    label_text = label_text.replace("\xa0","")
                                    label_text = label_text.strip()
                                    texto = texto.replace("\n","")
                                    texto = texto.replace("\xa0","")
                                    texto = texto.strip()
                                    info[label_text] = texto
                            if 'Mail de contacto' in info:
                                partner.write({'l10n_cl_dte_email': info['Mail de contacto'],'name':info['Razón Social/Nombres']})
