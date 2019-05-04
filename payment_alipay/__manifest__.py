# -*- coding: utf-8 -*-
{
    'name': "支付宝付款",
    'summary': """用于支付宝在线支付""",
    'description': """用于支付宝在线支付""",
    'author': "SuXueFeng",
    'website': "https://www.sxfblog.com",
    'category': 'alipay',
    'version': '1.0',
    'depends': ['payment', 'odoo_alipay', 'website_sale'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'views/payment_views.xml',
        'views/payment_sips_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    # 'post_init_hook': 'create_missing_journal_for_acquirers',

}