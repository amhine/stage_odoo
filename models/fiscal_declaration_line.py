from odoo import models, fields

class FiscalDeclarationLine(models.Model):
    _name = 'fiscal.declaration.line'
    _description = 'Ligne Déclaration Fiscale'

    declaration_id = fields.Many2one('fiscal.declaration', string='Déclaration', required=True, ondelete='cascade')
    code = fields.Char(string='Code Ligne', required=True)
    label = fields.Char(string='Libellé', required=True)
    amount = fields.Float(string='Montant')
