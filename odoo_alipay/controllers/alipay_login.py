# -*- coding: utf-8 -*-
import logging
from odoo import http, _
from odoo.addons.web.controllers.main import Home
from odoo.http import request
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')


class AliPayLogin(Home, http.Controller):

    @http.route('/web/alipay/login', type='http', auth='public', website=True, sitemap=False)
    def web_alipay_login(self, *args, **kw):
        """
        支付宝扫码、账号登录
        """
        # 拼接url
        url = request.env['alipay.system.conf'].sudo().search([('key', '=', 'oauth2_url')]).value
        alipay_appid = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_appid')
        # 回调地址
        redirect_uri = '{}web/alipay/get_auth_code'.format(request.httprequest.host_url)
        new_url = '{}?app_id={}&scope=auth_user&redirect_uri={}'.format(url, alipay_appid, redirect_uri)
        # 重定向到支付宝页面
        return http.redirect_with_hash(new_url)

    @http.route('/web/alipay/get_auth_code', type='http', auth="none")
    def alipay_get_auth_code(self, redirect=None, **kw):
        """
        支付宝登录回调方法
        """
        auth_code = request.params['auth_code']
        logging.info('>>>auth_code:{}'.format(auth_code))
        # 用得到的auth_code换取access_token及用户userId
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_gateway')
        alipay_client_config.app_id = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_appid')
        alipay_client_config.encrypt_key = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_aes')
        alipay_client_config.app_private_key = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_sign')
        alipay_client_config.alipay_public_key = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_public_key')
        self.get_access_token_and_userid(alipay_client_config, auth_code)

    def get_access_token_and_userid(self, alipay_client_config, auth_code):
        """
        设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
        """
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
        """
        系统接口：alipay.system.oauth.token
        """
        # 对照接口文档，构造请求对象
        from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest
        model = AlipaySystemOauthTokenRequest()
        model.grant_type = "authorization_code"
        model.code = auth_code
        result = client.execute(model)
        logging.info(">>>支付宝返回结果:{}".format(result))

