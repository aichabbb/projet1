# -*- coding: utf-8 -*-


{
    'name': "cheque ",

    'summary': """  """,

    'description': """ """,

    'author': "itadvisor",
    'website': "http://www.itadvisor.ma",

    'category': 'Uncategorized',
    'version': '12.0.0.0.1',
    'depends': ['base', 'mail','account'],

    # any module necessary for this one to work correctly
    # 'depends': ['base', 'contacts', 'hr'],

    # always loaded
    'data': [


        'security/ir.model.access.csv',
        'views/cheque.xml',
        'views/cheque_paiye.xml',
        'views/vue_ensemble.xml',
        'views/add_scss.xml',
        'data/sequence.xml',
        'data/data.xml',
        'wizards/depot.xml',


    ],

    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
