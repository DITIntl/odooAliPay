# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    alipay_appid = fields.Char(string='支付宝APPID')
    alipay_gateway = fields.Char(string='支付宝网关')
    alipay_aes = fields.Char(string='AES密钥')
    alipay_merchant_uid = fields.Char(string='商户UID')
    alipay_sign = fields.Text(string='应用私钥')

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            alipay_appid=self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_appid'),
            alipay_gateway=self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_gateway'),
            alipay_aes=self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_aes'),
            alipay_merchant_uid=self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_merchant_uid'),
            alipay_sign=self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_sign'),
        )
        return res

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('odoo_alipay.alipay_appid', self.alipay_appid)
        self.env['ir.config_parameter'].sudo().set_param('odoo_alipay.alipay_gateway', self.alipay_gateway)
        self.env['ir.config_parameter'].sudo().set_param('odoo_alipay.alipay_aes', self.alipay_aes)
        self.env['ir.config_parameter'].sudo().set_param('odoo_alipay.alipay_merchant_uid', self.alipay_merchant_uid)
        self.env['ir.config_parameter'].sudo().set_param('odoo_alipay.alipay_sign', self.alipay_sign)


