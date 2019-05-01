# -*- coding: utf-8 -*-
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    alipay_user_id = fields.Char(string='支付宝用户号')
    alipay_token = fields.Char(string='支付宝用户访问令牌')
    alipay_account = fields.Char(string='支付宝账号')
    alipay_real_name = fields.Char(string='支付宝真实姓名')

