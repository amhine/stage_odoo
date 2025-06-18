
from odoo import models, fields, api

class FiscalDeclarationLine(models.Model):
    _name = 'fiscal.declaration.line'
    _description = 'Ligne de Déclaration Fiscale'
    _order = 'sequence, id'
    
    declaration_id = fields.Many2one('fiscal.declaration', 'Déclaration', required=True, ondelete='cascade')
    sequence = fields.Integer('Séquence', default=10)
    
    code = fields.Char('Code', required=True)
    name = fields.Char('Libellé', required=True)
    amount = fields.Monetary('Montant', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='declaration_id.currency_id')
    
    line_type = fields.Selection([
        ('actif', 'Actif'),
        ('passif', 'Passif'),
        ('charge', 'Charge'),
        ('produit', 'Produit'),
        ('resultat', 'Résultat')
    ], string='Type de Ligne', required=True)
    
    account_ids = fields.Many2many('account.account', string='Comptes Associés')
    notes = fields.Text('Notes')
    
    @api.model
    def create(self, vals):
        if not vals.get('sequence'):
            last_line = self.search([('declaration_id', '=', vals.get('declaration_id'))], order='sequence desc', limit=1)
            vals['sequence'] = (last_line.sequence or 0) + 10
        return super().create(vals)