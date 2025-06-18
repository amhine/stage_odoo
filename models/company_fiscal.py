from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    dgi_identifier = fields.Char(string='Identifiant Fiscal DGI')
    regime_fiscal = fields.Selection([
        ('reel', 'Régime Réel'),
        ('simplifie', 'Régime Simplifié'),
        ('auto', 'Auto-entrepreneur')
    ], string='Régime Fiscal')
