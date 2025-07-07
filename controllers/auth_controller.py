from odoo import http
from odoo.http import request
import logging
import odoo

_logger = logging.getLogger(__name__)

class AuthController(http.Controller):
    
    @http.route('/fiscal/login', type='http', auth='public', website=True, csrf=False)
    def fiscal_login_page(self, **kw):
        """Affiche la page de connexion personnalisée"""
        if request.session.uid:
            return request.redirect('/fiscal/dashboard')
        
        values = {
            'error': kw.get('error', ''),
            'message': kw.get('message', ''),
            'login': kw.get('login', ''),
        }
        return request.render('ma_dgi_edi.auth_login_template', values)
    
    @http.route(['/fiscal/authenticate'], type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def fiscal_authenticate(self, **post):
        """Authentifie l'utilisateur sur la base testodoo"""
        try:
            login = post.get('login', '').strip()
            password = post.get('password', '')
            
            _logger.info(f"[AUTH] Tentative de connexion: {login}")
            
            if not login or not password:
                return request.redirect('/fiscal/login?error=Email et mot de passe requis')
            
            # Forcer la base de données dans la session
            request.session.db = 'testodoo'
            _logger.info(f"[AUTH] Base de données de la session: {request.session.db}")
            
            try:
                # Vérifier manuellement l'utilisateur dans la base testodoo
                registry = odoo.modules.registry.Registry('testodoo')
                with registry.cursor() as cr:
                    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                    user = env['res.users'].search([('login', '=', login)], limit=1)
                    if not user:
                        _logger.warning(f"[AUTH] Utilisateur non trouvé: {login}")
                        return request.redirect('/fiscal/login?error=Email ou mot de passe invalide')
                    
                    if not user.active:
                        _logger.warning(f"[AUTH] Utilisateur inactif: {login}")
                        return request.redirect('/fiscal/login?error=Compte utilisateur désactivé')
                    
                    # Vérifier le mot de passe
                    from passlib.context import CryptContext
                    crypt_context = CryptContext(schemes=['pbkdf2_sha512', 'plaintext'], deprecated=['plaintext'])
                    if user.password and crypt_context.verify(password, user.password):
                        # Configurer la session manuellement
                        request.session.db = 'testodoo'
                        request.session.uid = user.id
                        request.session.login = login
                        request.session.context = user.context_get()
                        _logger.info(f"[AUTH] Connexion réussie pour: {login} (UID: {user.id})")
                        return request.redirect('/fiscal/dashboard')
                    else:
                        _logger.warning(f"[AUTH] Mot de passe incorrect pour: {login}")
                        return request.redirect('/fiscal/login?error=Email ou mot de passe invalide')
                        
            except Exception as auth_error:
                _logger.error(f"[AUTH] Erreur méthode authenticate: {auth_error}")
                return request.redirect('/fiscal/login?error=Erreur de connexion')
                
        except Exception as e:
            _logger.error(f"[AUTH] Erreur lors de l'authentification: {e}")
            return request.redirect('/fiscal/login?error=Erreur de connexion')
    
    @http.route('/fiscal/logout', type='http', auth='user', website=True)
    def fiscal_logout(self, **kw):
        """Déconnecte l'utilisateur"""
        request.session.logout()
        return request.redirect('/fiscal/login?message=Déconnexion réussie')
    
    @http.route('/fiscal/dashboard', type='http', auth='user', website=True)
    def fiscal_dashboard(self, **kw):
        """Page d'accueil après connexion"""
        if not request.session.uid:
            return request.redirect('/fiscal/login')
        
        values = {
            'user': request.env.user,
        }
        return request.render('ma_dgi_edi.dashboard_template', values)