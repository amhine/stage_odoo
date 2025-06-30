from odoo import models, fields, api
from odoo.exceptions import UserError
import xml.etree.ElementTree as ET
from xml.dom import minidom
import base64

class EdiDocument(models.Model):
    _name = 'edi.document'
    _description = 'Document EDI'
    _order = 'create_date desc'
    
    name = fields.Char('Nom du Document', required=True)
    declaration_id = fields.Many2one('fiscal.declaration', 'Déclaration', required=True, ondelete='cascade')
    document_type = fields.Selection([
        ('bilan', 'Bilan'),
        ('cpc', 'Compte de Produits et Charges'),
        ('esg', 'État des Soldes de Gestion'),
        ('tableau_financement', 'Tableau de Financement'),
        ('etic', 'État des Informations Complémentaires')
    ], string='Type de Document', required=True)
    
    xml_content = fields.Text('Contenu XML')
    xml_file = fields.Binary('Fichier XML')
    file_name = fields.Char('Nom du Fichier')
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('generated', 'Généré'),
        ('validated', 'Validé'),
        ('sent', 'Envoyé')
    ], default='draft', string='État')
    
    validation_errors = fields.Text('Erreurs de Validation')
    generation_date = fields.Datetime('Date de Génération')
    
    def generate_xml(self):
        """Génère le contenu XML selon le format DGI"""
        try:
            xml_generator = self.env['dgi.xml.format']
            
            if self.document_type == 'bilan':
                xml_content = xml_generator._generate_bilan_xml(self.declaration_id)
            elif self.document_type == 'cpc':
                xml_content = xml_generator._generate_cpc_xml(self.declaration_id)
            elif self.document_type == 'esg':
                xml_content = xml_generator._generate_esg_xml(self.declaration_id)
            else:
                raise UserError(f"Type de document non supporté: {self.document_type}")
            
            self.xml_content = xml_content
            self.xml_file = base64.b64encode(xml_content.encode('utf-8'))
            self.file_name = f"{self.document_type}_{self.declaration_id.fiscal_year}.xml"
            self.generation_date = fields.Datetime.now()
            self.state = 'generated'
            
        except Exception as e:
            raise UserError(f"Erreur lors de la génération XML: {str(e)}")
    
    def validate_xml(self):
        """Valide le XML généré"""
        if not self.xml_content:
            raise UserError("Aucun contenu XML à valider.")
        
        try:
            ET.fromstring(self.xml_content)
            self.state = 'validated'
            self.validation_errors = False
        except ET.ParseError as e:
            self.validation_errors = f"Erreur de format XML: {str(e)}"
            raise UserError(self.validation_errors)
    
    def download_xml(self):
        """Télécharge le fichier XML"""
        if not self.xml_file:
            raise UserError("Aucun fichier XML généré.")
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/edi.document/{self.id}/xml_file/{self.file_name}?download=true',
            'target': 'self',
        }
