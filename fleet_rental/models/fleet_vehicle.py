from odoo import models, fields, api

class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _inherit = ['fleet.vehicle']

    tonnage = fields.Float(string="Tonelaje")
    fleet_fuel_ids = fields.One2many('fleet.vehicle.fuel','vehicle_id', string="Combustibles")
    fuel_count = fields.Integer(compute="_compute_count_fuel", string='Combustible')
    vehicule_license_id = fields.Many2one('fleet.vehicle.license',string="Matrícula")
    rigger_id = fields.Many2one('hr.employee', string="Rigger", domain="[('rigger_ok','=',True)]" )
    operator_id = fields.Many2one('hr.employee', string="Operario", domain="[('operator_ok','=',True)]")


    def copy_to_rental(self):
        for record in self:
            return  {
                'name': 'Asociar información a arriendo',
                'view_mode':'form',
                'view_type':'form',
                'res_model':'fleet.to.rental',
                'views': [(self.env.ref('fleet_rental.fleet_to_rental_form').id, 'form')],
                'context': {
                    'default_fleet_id': record.id,
                },
                'type':'ir.actions.act_window',
                'target': 'new',
        }

    def return_action_to_open_inherit(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:

            res = self.env['ir.actions.act_window']._for_xml_id('fleet_rental.%s' % xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
                domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False

    def _compute_count_fuel(self):
        fuel = self.env['fleet.vehicle.fuel']
        for record in self:
            record.fuel_count = fuel.search_count([('vehicle_id', '=', record.id)])

    @api.onchange('vehicule_license_id')
    def _onchange_license_plate(self):
        for record in self:
            if record.vehicule_license_id:
                record.license_plate = record.vehicule_license_id.name
