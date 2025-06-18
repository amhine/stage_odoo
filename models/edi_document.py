from odoo import models, fields

class EdiDocument(models.Model):
    _name = 'edi.document'
    _description = 'Document EDI'

    name = fields.Char(string='Nom', required=True)
    declaration_id = fields.Many2one('fiscal.declaration', string='Déclaration liée', required=True, ondelete='cascade')
    document_type = fields.Selection([
        ('bilan', 'Bilan'),
        ('cpc', 'Compte de Produits et Charges'),
        ('esg', 'État des Soldes de Gestion'),
        ('tf', 'Tableau de Financement')
    ], string='Type', required=True)
    file_name = fields.Char(string='Nom de fichier XML')
    xml_content = fields.Text(string='Contenu XML')
