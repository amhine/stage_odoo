from odoo import http, _
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class AuthController(http.Controller):
    
    @http.route('/fiscal/login', type='http', auth='public', website=True, csrf=False)
    def fiscal_login_page(self, **kw):
        """Page de connexion pour les déclarations fiscales"""
        
        if request.session.uid:
            return request.redirect('/fiscal/dashboard')
            
        values = {
            'error': kw.get('error', ''),
            'login': kw.get('login', ''),
        }
        return request.render('ma_dgi_edi.auth_login_template', values)

    @http.route('/fiscal/authenticate', type='http', auth='public', methods=['POST'], csrf=False)
    def fiscal_authenticate(self, **post):
        """Traitement de l'authentification"""
        email = post.get('email', '').strip()
        password = post.get('password', '')
        
        _logger.info(f"[AUTH DEBUG] Tentative connexion avec login='{email}'")
        
        if not email or not password:
            return self._redirect_with_error('Veuillez remplir tous les champs')
        
        try:
            db = request.session.db or request.env.cr.dbname
            uid = request.session.authenticate(db, email, password)
            
            if uid:
                user = request.env['res.users'].sudo().browse(uid)
                if user.exists() and user.active:
                    _logger.info(f"Connexion réussie pour l'utilisateur: {email}")
                    return request.redirect('/fiscal/dashboard')
                else:
                    _logger.warning(f"Utilisateur inactif ou inexistant: {email}")
                    return self._redirect_with_error('Compte utilisateur inactif')
            else:
                _logger.warning(f"Échec d'authentification pour: {email}")
                return self._redirect_with_error('Email ou mot de passe incorrect')
                
        except Exception as e:
            _logger.error(f"Erreur lors de l'authentification: {str(e)}")
            return self._redirect_with_error('Erreur lors de la connexion')

    @http.route('/fiscal/logout', type='http', auth='user')
    def fiscal_logout(self):
        """Déconnexion"""
        request.session.logout()
        return request.redirect('/fiscal/login')

    @http.route('/fiscal/dashboard', type='http', auth='user', website=True)
    def fiscal_dashboard(self):
        """Tableau de bord après connexion"""
        try:
            if not request.env.user or request.env.user._is_public():
                return request.redirect('/fiscal/login')
                
            return request.render('ma_dgi_edi.dashboard_template', {
                'user': request.env.user,
            })
        except Exception as e:
            _logger.error(f"Erreur dashboard: {str(e)}")
            return request.redirect('/fiscal/login?error=Erreur d\'accès au tableau de bord')

    def _redirect_with_error(self, error_message):
        """Rediriger avec message d'erreur"""
        import urllib.parse
        encoded_error = urllib.parse.quote(error_message)
        return request.redirect(f'/fiscal/login?error={encoded_error}')

    @http.route('/fiscal/forgot-password', type='http', auth='public', website=True)
    def forgot_password_page(self):
        """Page mot de passe oublié"""
        return request.render('ma_dgi_edi.forgot_password_template')

    @http.route('/fiscal/reset-password', type='http', auth='public', methods=['POST'], csrf=False)
    def reset_password(self, **post):
        """Traitement de la réinitialisation du mot de passe"""
        email = post.get('email', '').strip()
        
        if not email:
            return request.redirect('/fiscal/forgot-password?error=Veuillez saisir votre email')
        
        try:    
            user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if user:
                return request.redirect('/fiscal/login?message=Instructions envoyées par email')
            else:
                return request.redirect('/fiscal/forgot-password?error=Email non trouvé')
        except Exception as e:
            _logger.error(f"Erreur reset password: {str(e)}")
            return request.redirect('/fiscal/forgot-password?error=Erreur lors de la réinitialisation')