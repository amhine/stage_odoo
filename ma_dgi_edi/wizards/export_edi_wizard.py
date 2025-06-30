from odoo import models, fields, api
from odoo.exceptions import UserError
import zipfile
import io
import base64

class ExportEdiWizard(models.TransientModel):
    _name = 'export.edi.wizard'
    _description = 'Assistant d\'Export EDI'
    
    declaration_id = fields.Many2one('fiscal.declaration', 'Déclaration', required=True)
    export_format = fields.Selection([
        ('xml', 'XML Individuel'),
        ('zip', 'Archive ZIP'),
        ('dgi_package', 'Package DGI Complet')
    ], string='Format d\'Export', default='zip', required=True)
    
    include_validation = fields.Boolean('Inclure la Validation', default=True)
    add_digital_signature = fields.Boolean('Ajouter Signature Numérique', default=False)
    
    def action_export(self):
        """Exporte les documents EDI"""
        if self.declaration_id.state not in ['validated', 'submitted']:
            raise UserError("La déclaration doit être validée avant export.")
        
        if not self.declaration_id.edi_document_ids:
            raise UserError("Aucun document EDI généré pour cette déclaration.")
        
        if self.export_format == 'xml':
            return self._export_single_xml()
        elif self.export_format == 'zip':
            return self._export_zip_archive()
        else:
            return self._export_dgi_package()
    
    def _export_single_xml(self):
        """Exporte un seul fichier XML"""
        doc = self.declaration_id.edi_document_ids[0]
        if not doc.xml_file:
            doc.generate_xml()
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/edi.document/{doc.id}/xml_file/{doc.file_name}?download=true',
            'target': 'self',
        }
    
    def _export_zip_archive(self):
        """Exporte tous les documents dans une archive ZIP"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for doc in self.declaration_id.edi_document_ids:
                if not doc.xml_content:
                    doc.generate_xml()
                
                zip_file.writestr(doc.file_name, doc.xml_content)
        
        zip_data = base64.b64encode(zip_buffer.getvalue())
        zip_name = f"declaration_{self.declaration_id.fiscal_year}.zip"
        
        attachment = self.env['ir.attachment'].create({
            'name': zip_name,
            'type': 'binary',
            'datas': zip_data,
            'res_model': 'fiscal.declaration',
            'res_id': self.declaration_id.id,
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
    
    def _export_dgi_package(self):
        """Exporte un package complet DGI avec métadonnées"""
        return self._export_zip_archive()

