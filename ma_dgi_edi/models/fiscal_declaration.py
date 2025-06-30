from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class FiscalDeclaration(models.Model):
    _name = 'fiscal.declaration'
    _description = 'Déclaration Fiscale'
    _order = 'date_declaration desc'
    _rec_name = 'name'
    
    name = fields.Char('Référence', required=True, copy=False, default='/')
    company_id = fields.Many2one('res.company', 'Société', required=True, default=lambda self: self.env.company)
    fiscal_year = fields.Char('Exercice Fiscal', required=True)
    date_start = fields.Date('Date de Début', required=True)
    date_end = fields.Date('Date de Fin', required=True)
    date_declaration = fields.Date('Date de Déclaration', default=fields.Date.today, required=True)
    date_limit = fields.Date('Date Limite de Dépôt', required=True)
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
        ('submitted', 'Transmis'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté')
    ], default='draft', string='État', tracking=True)
    
    declaration_type = fields.Selection([
        ('complete', 'Déclaration Complète'),
        ('simplified', 'Déclaration Simplifiée')
    ], default='complete', string='Type de Déclaration', required=True)
    
    declaration_lines = fields.One2many('fiscal.declaration.line', 'declaration_id', 'Lignes de Déclaration')
    edi_document_ids = fields.One2many('edi.document', 'declaration_id', 'Documents EDI')
    
    notes = fields.Text('Notes')
    user_id = fields.Many2one('res.users', 'Utilisateur Responsable', default=lambda self: self.env.user)
    
    total_actif = fields.Monetary('Total Actif', compute='_compute_totals', store=True)
    total_passif = fields.Monetary('Total Passif', compute='_compute_totals', store=True)
    resultat_net = fields.Monetary('Résultat Net', compute='_compute_totals', store=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('fiscal.declaration') or '/'
        return super().create(vals)
    
    @api.depends('declaration_lines.amount')
    def _compute_totals(self):
        for record in self:
            actif_lines = record.declaration_lines.filtered(lambda l: l.line_type == 'actif')
            passif_lines = record.declaration_lines.filtered(lambda l: l.line_type == 'passif')
            resultat_lines = record.declaration_lines.filtered(lambda l: l.line_type == 'resultat')
            
            record.total_actif = sum(actif_lines.mapped('amount'))
            record.total_passif = sum(passif_lines.mapped('amount'))
            record.resultat_net = sum(resultat_lines.mapped('amount'))
    
    def action_validate(self):
        """Valide la déclaration fiscale"""
        self._validate_declaration_data()
        self.state = 'validated'
        self._generate_edi_documents()
    
    def action_submit(self):
        """Soumet la déclaration à la DGI"""
        if self.state != 'validated':
            raise UserError("La déclaration doit être validée avant soumission.")
        
        self.state = 'submitted'
        self._send_notification_email()
    
    def action_reset_to_draft(self):
        """Remet la déclaration en brouillon"""
        self.state = 'draft'
    
    def _validate_declaration_data(self):
        """Valide les données de la déclaration"""
        if not self.declaration_lines:
            raise ValidationError("La déclaration doit contenir au moins une ligne.")
        
        if self.date_start >= self.date_end:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")
        
        if self.date_declaration > self.date_limit:
            raise ValidationError("La date de déclaration ne peut pas dépasser la date limite.")
    
    def _generate_edi_documents(self):
        """Génère les documents EDI"""
        edi_model = self.env['edi.document']
        
        bilan_doc = edi_model.create({
            'name': f'Bilan {self.fiscal_year}',
            'declaration_id': self.id,
            'document_type': 'bilan',
        })
        bilan_doc.generate_xml()
        
        cpc_doc = edi_model.create({
            'name': f'CPC {self.fiscal_year}',
            'declaration_id': self.id,
            'document_type': 'cpc',
        })
        cpc_doc.generate_xml()
    
    def _send_notification_email(self):
        """Envoie un email de notification"""
        template = self.env.ref('ma_dgi_edi.email_template_declaration_submitted', False)
        if template:
            template.send_mail(self.id, force_send=True)