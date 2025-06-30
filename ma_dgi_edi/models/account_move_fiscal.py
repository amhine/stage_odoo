from odoo import models, fields, api

class AccountMoveFiscal(models.Model):
    _inherit = 'account.move'
    
    fiscal_declaration_id = fields.Many2one('fiscal.declaration', 'Déclaration Fiscale')
    is_fiscal_relevant = fields.Boolean('Pertinent Fiscalement',default=True)   
    fiscal_notes = fields.Text('Notes Fiscales')
    
    def action_add_to_fiscal_declaration(self):
        """ajoute l'écriture a une declaration fiscale""" 
        return {
            'type':'ir.actions.act_window',
            'name': 'Ajouter a la declaration fiscale',
            'res_mode':'add.to.declaration.wizard',
            'view_mode': 'form',
            'target':'new',
            'context':{'default_move_ids':[(6,0,self.ids)]}
        }