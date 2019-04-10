# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    din_agentid = fields.Char(string=u'AgentId')
    din_corpId = fields.Char(string=u'企业CorpId')
    din_appkey = fields.Char(string=u'AppKey')
    din_appsecret = fields.Char(string=u'AppSecret')
    din_token = fields.Boolean(string="自动获取Token")
    din_create_extcontact = fields.Boolean(string=u'添加外部联系人')
    din_update_extcontact = fields.Boolean(string=u'修改外部联系人')
    din_delete_extcontact = fields.Boolean(string=u'删除外部联系人')
    din_create_employee = fields.Boolean(string=u'添加员工')
    din_update_employee = fields.Boolean(string=u'修改员工')
    din_delete_employee = fields.Boolean(string=u'删除员工')
    din_create_department = fields.Boolean(string=u'添加部门')
    din_update_department = fields.Boolean(string=u'修改部门')
    din_delete_department = fields.Boolean(string=u'删除部门')
    din_login_appid = fields.Char(string=u'扫码登录appId')
    din_login_appsecret = fields.Char(string=u'扫码登录appSecret')

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            din_agentid=self.env['ir.config_parameter'].sudo().get_param('ali_dindin.din_agentid'),
        )
        return res

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('ali_dindin.din_agentid', self.din_agentid)


