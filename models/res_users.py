from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    tax_id = fields.Char('Identifiant Fiscal', help='Numéro d\'identification fiscale')
    phone_verified = fields.Boolean('Téléphone Vérifié', default=False)
    is_tax_declarant = fields.Boolean('Déclarant Fiscal', default=False)
    
    @api.constrains('login')
    def _check_email_format(self): 
        """Valider le format email"""
        for user in self:
            if user.login and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user.login):
                raise ValidationError("Format d'email invalide")