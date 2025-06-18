from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    included_in_declaration = fields.Boolean(string='Inclure dans la Déclaration Fiscale', default=True)
