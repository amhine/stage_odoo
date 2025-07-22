# ma_dgi_edi/controllers/fiscal_declaration_controller.py
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

    @http.route('/fr/fiscal/new-declaration', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def new_declaration(self, **kwargs):
        user = request.env.user
        is_accountant = user.has_group('ma_dgi_edi.group_accountant')

        #if is_accountant:
         #   return request.redirect('/fr/fiscal/declarations')  

        companies = request.env['res.company'].search([])

        if request.httprequest.method == 'POST':
            values = {
                'name': kwargs.get('name'),
                'declaration_type': kwargs.get('declaration_type'),
                'month': kwargs.get('month'),
                'exercise': kwargs.get('exercise'),
                'company_id': int(kwargs.get('company_id')) if kwargs.get('company_id') else False,
                'user_id': user.id,
                'status': 'draft',
            }
            request.env['fiscal.declaration'].create(values)
            return request.redirect('/fr/fiscal/declarations')

        return request.render('ma_dgi_edi.new_declaration_template', {
            'companies': companies,
            'is_accountant': is_accountant,
        })

class FiscalDeclarationActivateController(http.Controller):
    @http.route('/fr/fiscal/activate/<int:declaration_id>', type='http', auth='user', website=True)
    def activate_declaration(self, declaration_id, **kwargs):
        declaration = request.env['fiscal.declaration'].browse(declaration_id)
        if declaration.user_id.id == request.env.user.id and declaration.status == 'draft':
            declaration.write({'status': 'activated'})
        return request.redirect('/fr/fiscal/declarations')