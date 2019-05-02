# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AliPayUser(models.Model):
    _description = '用户/会员列表'
    _name = 'alipay.users'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(string='用户名称')
    login_id = fields.Char(string='登录账号')
    user_id = fields.Char(string='用户Id')
    user_type = fields.Selection(string=u'用户类型', selection=[('PRIVATE', '个人用户'), ('CORPORATE', '企业用户')])
    
