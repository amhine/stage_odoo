{
    'name': "DGI",
    'version': '18.0.0.1.0',
    'summary': 'Module EDI pour la DGI',
    'description': 'Génération et télédéclaration des liasses fiscales en XML',
    'author': "Nihad",
    'category': 'Accounting',
    'depends': [
        'base',
        'web',  # utile si tu utilises des assets ou des contrôleurs
    ],
    'data': [
        'views/auth_template.xml',
    ],
    'assets': {
    'web.assets_frontend': [
        'ma_dgi_edi/static/src/css/auth_style.css',
        'ma_dgi_edi/static/src/js/auth.js',
    ],
},

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
