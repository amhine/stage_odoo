{
    'name': 'Morocco DGI EDI - Télédéclaration Fiscale',
    'summary': 'Génération des liasses fiscales conformes aux exigences de la DGI du Maroc',
    'description': """
        Module de génération XML EDI pour la déclaration fiscale (liasse) selon la norme marocaine.
        Inclut la configuration des sociétés, des déclarations et des exports.
    """,
    'version': '18.0.1.0.0',
    'author': 'Ton Nom / Entreprise',
    'license': 'AGPL-3',
    'website': 'https://tonsite.com',
    'category': 'Accounting/Localizations',
    'depends': ['base', 'account', 'l10n_ma'],
    'data': [

        'security/ir.model.access.csv',
        'security/fiscal_security.xml',


        'data/fiscal_forms_data.xml',
        'data/sequence_data.xml',
        'data/email_templates.xml',


        'views/fiscal_declaration_views.xml',
        'views/edi_document_views.xml',
        'views/company_fiscal_views.xml',
        'views/menus.xml',


        'wizards/generate_declaration_wizard.xml',
        'wizards/import_declaration_wizard.xml',
        'wizards/export_edi_wizard.xml',


        'reports/fiscal_declaration_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ma_dgi_edi/static/src/css/style.css',
            'ma_dgi_edi/static/src/js/main.js',
        ],
    },
}
