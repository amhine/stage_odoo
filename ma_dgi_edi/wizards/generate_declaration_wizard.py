from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class GenerateDeclarationWizard(models.TransientModel):
    _name = 'generate.declaration.wizard'
    _description = 'Assistant de Génération de Déclaration'
    
    company_id = fields.Many2one('res.company', 'Société', required=True, default=lambda self: self.env.company)
    fiscal_year = fields.Char('Exercice Fiscal', required=True, default=lambda self: str(datetime.now().year))
    date_start = fields.Date('Date de Début', required=True)
    date_end = fields.Date('Date de Fin', required=True)
    
    declaration_type = fields.Selection([
        ('complete', 'Déclaration Complète'),
        ('simplified', 'Déclaration Simplifiée')
    ], string='Type de Déclaration', required=True, default='complete')
    
    include_movements = fields.Boolean('Inclure les Écritures Comptables', default=True)
    date_limit = fields.Date('Date Limite de Dépôt', required=True)
    
    @api.onchange('fiscal_year')
    def _onchange_fiscal_year(self):
        if self.fiscal_year:
            year = int(self.fiscal_year)
            self.date_start = datetime(year, 1, 1).date()
            self.date_end = datetime(year, 12, 31).date()
            self.date_limit = datetime(year + 1, 3, 31).date()  
    
    def action_generate(self):
        """Génère la déclaration fiscale"""
        if self.date_start >= self.date_end:
            raise UserError("La date de début doit être antérieure à la date de fin.")
        
        declaration = self.env['fiscal.declaration'].create({
            'company_id': self.company_id.id,
            'fiscal_year': self.fiscal_year,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'date_limit': self.date_limit,
            'declaration_type': self.declaration_type,
        })
        
        if self.include_movements:
            self._generate_declaration_lines(declaration)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Déclaration Fiscale',
            'res_model': 'fiscal.declaration',
            'res_id': declaration.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def _generate_declaration_lines(self, declaration):
        """Génère les lignes de déclaration basées sur les données comptables"""
        accounts = self.env['account.account'].search([
            ('company_id', '=', self.company_id.id),
            ('code', 'like', '1%'),  
        ])
        
        lines_to_create = []
        
        for account in accounts:
            balance = self._get_account_balance(account, self.date_start, self.date_end)
            if balance != 0:
                line_type = self._determine_line_type(account.code)
                lines_to_create.append({
                    'declaration_id': declaration.id,
                    'code': account.code,
                    'name': account.name,
                    'amount': balance,
                    'line_type': line_type,
                    'account_ids': [(6, 0, [account.id])],
                })
        
        self.env['fiscal.declaration.line'].create(lines_to_create)
    
    def _get_account_balance(self, account, date_start, date_end):
        """Calcule le solde d'un compte sur une période"""
        domain = [
            ('account_id', '=', account.id),
            ('date', '>=', date_start),
            ('date', '<=', date_end),
            ('move_id.state', '=', 'posted')
        ]
        
        move_lines = self.env['account.move.line'].search(domain)
        return sum(move_lines.mapped('balance'))
    
    def _determine_line_type(self, account_code):
        """Détermine le type de ligne selon le code comptable"""
        if account_code.startswith('1') or account_code.startswith('2') or account_code.startswith('3'):
            return 'actif'
        elif account_code.startswith('4') or account_code.startswith('5'):
            return 'passif'
        elif account_code.startswith('6'):
            return 'charge'
        elif account_code.startswith('7'):
            return 'produit'
        else:
            return 'resultat'

#