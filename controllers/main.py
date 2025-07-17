from odoo import http
from odoo.http import request

class FiscalDeclarationController(http.Controller):
    @http.route('/fr/fiscal/declarations', type='http', auth='user', website=True)
    def fiscal_declarations(self, **kwargs):
        user = request.env.user
        is_accountant = user.has_group('ma_dgi_edi.group_accountant')

        if is_accountant:
            clients = request.env['res.users'].sudo().search([
                ('accountant_id', '=', user.id)
            ])
            declarations = request.env['fiscal.declaration'].sudo().search([
                ('user_id', 'in', clients.ids),
                ('status', '=', 'accepted')
            ])
            users = clients  
        else:
            declarations = request.env['fiscal.declaration'].search([
                ('user_id', '=', user.id)
            ])
            users = []

        return request.render('ma_dgi_edi.declarations_template', {
            'declarations': declarations,
            'users': users,
            'is_accountant': is_accountant,
        })
        
        
