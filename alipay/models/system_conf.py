# -*- coding: utf-8 -*-
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class AliPayPayConfig(models.Model):
    _description = '系统参数列表'
    _name = 'alipay.system.conf'

    name = fields.Char(string='名称')
    key = fields.Char(string='key值')
    value = fields.Char(string='参数值')
    company_id = fields.Many2one(comodel_name='res.company', string=u'公司',
                                 default=lambda self: self.env.user.company_id.id, required=True)

    _sql_constraints = [
        ('key_uniq', 'unique(key)', u'系统参数中key值不允许重复!'),
    ]

