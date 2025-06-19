from odoo import models,fields,api
from odoo.exceptions import UserError
from datetime import timedelta
import base64
import xml.etree.ElementTree as ET

class ImportDeclarationWizard(models.TransientModel):
    _name = 'import.declaration.wizard'
    _description = 'Assistant d\Importation de declaration'
    
    xml_file = fields.Binary('Fichier XML', required = True)
    xml_filename = fields.Char('nom du fichier')
    company_id = fields.Many2one('res.company','société',required=True , default=lambda self:self.env.company)
    def action_import(self):
        """Importe une déclaration depuis un fichier Xml"""
        if not self.xml_file:
            raise UserError("veuiller selectionner un fichier XML")
        try:
            xml_content = base64.b64decode(self.xml_file).decode('utf-8')
            root = ET.fromstring(xml_content)
            
            fiscal_year = root.get('exercice', str(fields.Date.today().year))
            
            declaration = self.env['fiscal.declaration'].create({
                'company_id': self.company_id.id,
                'fiscal_year': fiscal_year,
                'date_start': fields.Date.today().replace(month=1, day=1),
                'date_end': fields.Date.today().replace(month=12, day=31),
                'date_limit': fields.Date.today() + timedelta(days=90),
                'declaration_type': 'complete',
            })
            
            self._parse_xml_lines(root, declaration)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Déclaration Importée',
                'res_model': 'fiscal.declaration',
                'res_id': declaration.id,
                'view_mode': 'form',
                'target': 'current',
            }
            
        except Exception as e:
            raise UserError(f"Erreur lors de l'importation: {str(e)}")
    
    def _parse_xml_lines(self, root, declaration):
        """Parse les lignes du XML et les crée dans la déclaration"""
        lines_to_create = []
        
        for element in root.iter():
            if element.tag in ['ACTIF', 'PASSIF', 'CHARGE', 'PRODUIT']:
                code = element.get('code', '')
                name = element.get('libelle', element.tag)
                amount = float(element.text or '0')
                
                if amount != 0:
                    lines_to_create.append({
                        'declaration_id': declaration.id,
                        'code': code,
                        'name': name,
                        'amount': amount,
                        'line_type': element.tag.lower(),
                    })
        
        if lines_to_create:
            self.env['fiscal.declaration.line'].create(lines_to_create)