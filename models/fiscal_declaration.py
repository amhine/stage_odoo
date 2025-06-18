from odoo import models, fields, api

class FiscalDeclaration(models.Model):
    _name = 'fiscal.declaration'
    _description = 'Déclaration Fiscale'
    _order = 'date_declaration desc'

    name = fields.Char(string='Référence', required=True, default='/', copy=False)
    company_id = fields.Many2one('res.company', string='Société', required=True, default=lambda self: self.env.company)
    fiscal_year = fields.Char(string='Exercice Fiscal', required=True)
    date_declaration = fields.Date(string='Date de Déclaration', default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
        ('submitted', 'Soumis'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté')
    ], string='État', default='draft')

    declaration_line_ids = fields.One2many('fiscal.declaration.line', 'declaration_id', string='Lignes')
    edi_document_ids = fields.One2many('edi.document', 'declaration_id', string='Documents EDI')
