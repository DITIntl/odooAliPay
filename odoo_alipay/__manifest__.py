# -*- coding: utf-8 -*-
{
    'name': "阿里-支付宝",
    'summary': """阿里-支付宝""",
    'description': """阿里-支付宝""",
    'author': "SuXueFeng",
    'website': "https://www.sxfblog.com",
    'category': 'alipay',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/alipay_groups.xml',
        'security/ir.model.access.csv',
        'data/system_conf.xml',
        'data/default_num.xml',
        'views/menu.xml',
        'views/res_config_settings_views.xml',
        'views/merchant_account.xml',
        'views/res_partner.xml',
        'views/system_conf.xml',
        'views/login_templates.xml',
        'views/transfer.xml',
    ],

}
