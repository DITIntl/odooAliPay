# -*- coding: utf-8 -*-
import logging
from odoo import http, _
from odoo.addons.web.controllers.main import Home
from odoo.http import request
from urllib.parse import quote

import traceback
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel

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
        logging.info('----支付宝登录回调方法-----------')
        logging.info('auth_code:{}'.format(auth_code))
        logging.info('--------------------------')
        # 用得到的auth_code换取access_token及用户userId
        alipay_gateway = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_gateway')
        alipay_appid = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_appid')
        alipay_sign = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_sign')
        alipay_aes = request.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_aes')
        self.get_access_token_and_userid(alipay_gateway, alipay_appid, alipay_sign, alipay_aes, auth_code)

    def get_access_token_and_userid(self, alipay_gateway, alipay_appid, alipay_sign, alipay_aes, auth_code):
        """
        设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
        """
        alipay_client_config = AlipayClientConfig()
        print(alipay_gateway)
        print(alipay_appid)
        print(alipay_sign)
        print(alipay_aes)
        print("-----------------")
        alipay_client_config.server_url = alipay_gateway
        alipay_client_config.app_id = alipay_appid
        alipay_client_config.app_private_key = alipay_aes
        alipay_client_config.alipay_public_key = alipay_sign
        """
        得到客户端对象。
        注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，
        如果想使用不同的配置，请定义不同的DefaultAlipayClient。logger参数用于打印日志，不传则不打印，建议传递。
        """
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
        """
        系统接口示例：alipay.trade.pay
        """
        #     # 对照接口文档，构造请求对象
        #     alipay.system.oauth.token

        from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest
        from alipay.aop.api.response.AlipaySystemOauthTokenResponse import AlipaySystemOauthTokenResponse
        model = AlipaySystemOauthTokenRequest()
        model.grant_type = "authorization_code"
        model.code = auth_code
        result = client.execute(model)
        print(result)

