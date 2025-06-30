from odoo import models,fields,api

class CompanyFiscal(models.Model):
    _inherit='res.company'
    
    dgi_identifier = fields.Char('Identifiant DGI',help="Identifiant unique  de la DGI")
    tax_regime = fields.Selection([
        ('normal', 'Régime Normal'),
        ('simplified','Régime Simplifié'),
        ('auto_entrepreneur','Auto-Entrepreneur')
    ],string='Régime Fiscal', default='normal')
    
    fiscal_year_end = fields.Selection([
        ('12-31', '31 Décembre'),
        ('06-30', '30 Juin'),
        ('03-31', '31 Mars'),
        ('09-30', '30 Septembre')
    ], string='Fin d\'Exercice Fiscal', default='12-31')
    
    edi_enabled = fields.Boolean('EDI Activé',default=True)
    edi_test_mode = fields.Boolean('Mode Test EDI',default=True)
    edi_certificate = fields.Binary('Certificat EDI')
    edi_certificate_name = fields.Char('Nom du Certificat')
    
    fiscal_responsable = fields.Many2one('res.users','Responsable Fiscal')
    accountant_contact = fields.Many2one('res.partner','Contact Comptable')