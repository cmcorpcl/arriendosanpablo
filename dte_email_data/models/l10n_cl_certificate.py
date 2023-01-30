from odoo import api, fields, models,_
from bs4 import BeautifulSoup
import base64
from requests_pkcs12 import get
from cryptography.fernet import Fernet

class l10nclCertificate(models.Model):
    _inherit = "l10n_cl.certificate"

    compute_encrypt_pass = fields.Char('Llave encryptada', compute="compute_encrypt_key")
    encrypt_pass = fields.Char('Llave encryptada')
    key_encrypt= fields.Char('Key')
    priority_dte = fields.Boolean(string="Usar como prioridad para obtener datos clientes")
    only_dte = fields.Boolean(string="Solo para DTE")

    @api.depends('signature_pass_phrase')
    def compute_encrypt_key(self):
        for record in self:
            record.compute_encrypt_pass = ""
            if record.signature_pass_phrase:
                key = Fernet.generate_key()
                if record.key_encrypt:
                    key = record.key_encrypt.encode()
                key_change = key.decode() + "546"
                final_key = key_change.encode()
                fernet = Fernet(final_key)
                enc_message = fernet.encrypt((record.signature_pass_phrase).encode())
                decMessage = fernet.decrypt(enc_message).decode()
                record.compute_encrypt_pass = enc_message
                record.encrypt_pass = enc_message
                if not record.key_encrypt:
                    record.key_encrypt = key
