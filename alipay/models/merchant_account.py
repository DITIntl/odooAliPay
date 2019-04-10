# -*- coding: utf-8 -*-
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class MerchantAccount(models.Model):
    _description = '商户账号'
    _name = 'alipay.merchant.account'

    name = fields.Char(string='商家名称', required=True)
    account = fields.Char(string='商家账号', required=True)
    uid = fields.Char(string='商户UID')
    pwd = fields.Char(string='登录密码')
    company_id = fields.Many2one(comodel_name='res.company', string=u'公司',
                                 default=lambda self: self.env.user.company_id.id, required=True)
    state = fields.Selection(string=u'有效', selection=[('y', '有效'), ('n', '无效'), ], default='y', required=True)

    _sql_constraints = [
        ('account_uniq', 'unique(account)', u'商家账号不允许重复!'),
        ('uid_uniq', 'unique(uid)', u'商家账号不允许重复!'),
    ]