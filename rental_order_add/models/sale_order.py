from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

YESNO=[
    ('yes','Si'),
    ('no','No'),
]
PAYOPT=[
    ('efectivo','Efectivo'),
    ('cheque','Cheque'),
    ('transferencia','Transferencia'),
    ('credito','Credito'),
]
RENTALSTATEASP = [
    ('cancelado','Cancelado'),
    ('cotizacion','Cotizacion'),
    ('cotizacion_pendiente','Cotizacion Pendiente'),
    ('requerimiento','Requerimiento'),
    ('requerimiento_pendiente','Requerimiento Pendiente'),
    ('orden_de_trabajo','Orden de Trabajo'),
    ('poder_cliente','En el poder del cliente'),
    ('devuelto','Devuelto'),
]
TOAUTORIZED = [
    ('a_autorizar','A autorizar'),
    ('autorizado','Autorizado')

]

CLIENTORUS = [
    ('cliente','Cliente'),
    ('san_pablo','San Pablo')
]
CLIENTTYPE = [
    ('antiguo','Antiguo'),
    ('nuevo','Nuevo')
]
GUARANTEEDOC = [
    ('cheque','Cheque'),
    ('transferencia','Transferencia'),
    ('sin_garantia','Sin Garantía')
]

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']

    work_address = fields.Text(string='Dirección de obra')
    work_city = fields.Char(string='Ciudad de obra')
    work_partner = fields.Char(string='Contacto de obra')
    work_email = fields.Char(string='Correo de contacto')
    work_phone = fields.Char(string='Telefono de contacto')
    route_from = fields.Char(string='Ruta desde')
    route_to = fields.Char(string='Ruta hasta')
    total_km = fields.Float(string='Total KM')
    with_fuel = fields.Selection(CLIENTORUS,string='Combustible' )
    work_meal = fields.Selection(CLIENTORUS,string="Alimentación" )
    work_lodging = fields.Selection(CLIENTORUS,string="Alojamiento" )
    work_rigger = fields.Selection(CLIENTORUS,string="Rigger")
    payment_options = fields.Selection(PAYOPT,string="Opcion de pago", default="efectivo")

    type_client = fields.Selection(CLIENTTYPE,string='Tipo cliente',default="antiguo")
    with_contract = fields.Selection(YESNO,string="Contrato", default="no")
    document_type_guaranty = fields.Selection(GUARANTEEDOC,string='Tipo documento en garantía', default="cheque")
    dicom = fields.Selection(YESNO,string='Reviso Situación Financiera (Dicom)', default="no")
    validate_document_guaranty = fields.Selection(YESNO,string='Reviso Situación Documento garantía', default="no")
    autorized_credit = fields.Selection(YESNO,string='Si es cliente credito esta autorizado', default="no")
    who_autorized = fields.Char(string='Quien autoriza Credito')
    who_autorized_id = fields.Many2one('hr.employee',string='Quien autoriza Credito', domain="[('autorized_credit','=',True)]")

    fuel_odometer_ids = fields.One2many('fuel.odometer','sale_id',string="Combustible/Odometro")

    is_autorized = fields.Boolean(string="Autorizar")
    state_autorized = fields.Selection(TOAUTORIZED,string="Estado Autorización comp",compute="_compute_state_autorized")
    state_autorized_store = fields.Selection(TOAUTORIZED,string="Estado Autorización", default="a_autorizar")

    state_rental_asp = fields.Selection(RENTALSTATEASP,string="Estado ASP comp",compute="_compute_state_rental_asp")
    state_rental_asp_store = fields.Selection(RENTALSTATEASP,string="Estado ASP", default="requerimiento")

    is_requirement = fields.Boolean(string="Es requerimiemto", readonly=True)

    diary_minimum_hours = fields.Float(string="Horas minimas diarias")
    month_minimum_hours = fields.Float(string="Horas minimas mensuales")
    hour_price = fields.Float(string="Precio Hora")

    note_operator = fields.Text(string="Detalle Servicio")

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        for record in self:
            if record.is_rental_order:
                list_name_work = [
                    'work_address','work_city','work_partner','work_email','work_phone',
                    'route_from','route_to','total_km']
                for name in list_name_work:
                    for ans in record.mapped(name):
                        if not ans:
                            raise ValidationError(_("No se han ingresado todos los datos para transformar a requerimiento, revise el dato '{}'.".format(record._fields[name].string)))
            record.is_autorized = True
            record.is_requirement = True
        return result


    def make_requirement(self):
        for record in self:
            list_name_work = [
                'work_address','work_city','work_partner','work_email','work_phone',
                'route_from','route_to','total_km']
            for name in list_name_work:
                for ans in record.mapped(name):
                    if not ans:
                        raise ValidationError(_("No se han ingresado todos los datos para transformar a requerimiento, revise el dato '{}'.".format(record._fields[name].string)))
            record.is_requirement = True


    @api.depends('state')
    def _compute_state_rental_asp(self):
        for record in self:
            record.state_rental_asp = "cotizacion"
            if record.state == "draft":
                record.state_rental_asp = "cotizacion"
                record.state_rental_asp_store = "cotizacion"
            elif record.state == "cancel":
                record.state_rental_asp = "cancelado"
                record.state_rental_asp_store = "cancelado"
            elif record.state == "sent" and not record.is_requirement:
                record.state_rental_asp = "cotizacion_pendiente"
                record.state_rental_asp_store = "cotizacion_pendiente"
            elif record.state == "sent" and record.is_requirement:
                record.state_rental_asp = "requerimiento_pendiente"
                record.state_rental_asp_store = "requerimiento_pendiente"
            elif record.state in ["sale","done"]:
                record.state_rental_asp = "orden_de_trabajo"
                record.state_rental_asp_store = "orden_de_trabajo"
                if record.rental_status == "return":
                    record.state_rental_asp = "poder_cliente"
                    record.state_rental_asp_store = "poder_cliente"
                elif record.rental_status == "returned":
                    record.state_rental_asp = "devuelto"
                    record.state_rental_asp_store = "devuelto"

    @api.depends('is_autorized')
    def _compute_state_autorized(self):
        for record in self:
            record.state_autorized = "a_autorizar"
            record.state_autorized_store = "a_autorizar"
            if  record.is_autorized:
                record.state_autorized = "autorizado"
                record.state_autorized_store = "autorizado"
