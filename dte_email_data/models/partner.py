from odoo import api, fields, models,_
from bs4 import BeautifulSoup
import base64
from requests_pkcs12 import get
from cryptography.fernet import Fernet

class ResPartner(models.Model):
    _inherit = "res.partner"


    @api.onchange('vat')
    def change_dte_email(self):
        for record in self:
            if record.vat:
                cert_file = False
                cert_pass = False
                vat = record.vat
                vat = vat.replace(" ","")
                vat = vat.replace(".","")
                vat = vat.upper()
                if vat[0] == '0':
                    vat = vat[1:]
                dte_partner_env= self.env['dte_email_data.dte_partner']
                dte_partner_encounter = dte_partner_env.search([('rut','=', vat)])
                if(len(dte_partner_encounter) > 0):
                    record.l10n_cl_dte_email = dte_partner_encounter[0].dte_email
                    record.name = dte_partner_encounter[0].bussiness_line
                else:
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
                        if cert_file and cert_pass:
                            r = get("https://palena.sii.cl/cvc_cgi/dte/ce_consulta_rut", pkcs12_data=base64.b64decode(cert_file),pkcs12_password=cert_pass)
                            cookies = r.cookies
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
                                    record.l10n_cl_dte_email = info['Mail de contacto']
                                    record.name =info['Razón Social/Nombres']
                        else:
                            return {
                                'type': 'ir.actions.client',
                                'tag': 'display_notification',
                                'params': {
                                    'title': _('Warning'),
                                    'message':  'Revisar certificado SII',
                                    'type': 'danger',  #types: success,warning,danger,info
                                    'sticky': False,
                                }
                            }
