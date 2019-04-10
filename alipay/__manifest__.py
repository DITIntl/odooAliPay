# -*- coding: utf-8 -*-
{
    'name': "阿里-支付宝",
    'summary': """阿里-支付宝""",
    'description': """阿里-支付宝""",
    'author': "SuXueFeng",
    'website': "https://www.sxfblog.com",
    'category': 'alipay',
    'version': '1.0',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'security/alipay_groups.xml',
        'data/system_conf.xml',
        'views/menu.xml',
        'views/res_config_settings_views.xml',
        'views/merchant_account.xml',
        'views/system_conf.xml',
    ],

}
