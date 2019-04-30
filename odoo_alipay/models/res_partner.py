# -*- coding: utf-8 -*-
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    alipay_user_id = fields.Char(string='支付宝用户Id')
    alipay_token = fields.Char(string='支付宝用户访问令牌')

