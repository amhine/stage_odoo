from odoo import models, fields, api

class FiscalDeclaration(models.Model):
    _name = 'fiscal.declaration'
    _description = 'Fiscal Declaration'

    name = fields.Char(string='Declaration Name', required=True)
    declaration_type = fields.Selection([
        ('tva', 'TVA'),
        ('is', 'Impôt sur les Sociétés'),
        ('ir', 'Impôt sur le Revenu'),
    ], string='Type', required=True)
    month = fields.Selection([
        ('01', 'Janvier'), ('02', 'Février'), ('03', 'Mars'),
        ('04', 'Avril'), ('05', 'Mai'), ('06', 'Juin'),
        ('07', 'Juillet'), ('08', 'Août'), ('09', 'Septembre'),
        ('10', 'Octobre'), ('11', 'Novembre'), ('12', 'Décembre'),
    ], string='Mois', required=True)
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('activated', 'Activé'),
        ('accepted', 'Accepté'),
        ('sent', 'Envoyé'),
    ], string='Statut', default='draft')
    exercise = fields.Char(string='Exercice', required=True)
    company_id = fields.Many2one('res.company', string='Société', required=True)
    turnover = fields.Float(string='Chiffre d\'affaires', compute='_compute_turnover', store=True)
    dgi_reference = fields.Char(string='Référence DGI')
    creation_date = fields.Datetime(string='Créé le', default=fields.Datetime.now)
    sent_date = fields.Datetime(string='Envoyé le')
    user_id = fields.Many2one('res.users', string='Utilisateur', default=lambda self: self.env.user)

    @api.depends('company_id', 'month', 'exercise')
    def _compute_turnover(self):
        for record in self:
            # Placeholder logic for automatic turnover calculation
            # Replace with actual logic based on your accounting module or DGI requirements
            record.turnover = 0.0  # Example: Fetch from accounting entries