from odoo import http
from odoo.http import request

class FiscalDeclarationActivateController(http.Controller):
    @http.route('/fr/fiscal/activate/<int:declaration_id>', type='http', auth='user', website=True)
    def activate_declaration(self, declaration_id, **kwargs):
        declaration = request.env['fiscal.declaration'].browse(declaration_id)
        if declaration.user_id.id == request.env.user.id and declaration.status == 'draft':
            declaration.write({'status': 'activated'})
        return request.redirect('/fr/fiscal/declarations')