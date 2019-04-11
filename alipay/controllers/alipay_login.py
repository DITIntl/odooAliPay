# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import logging
import time
import requests
from requests import ReadTimeout
from odoo import http, _
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.http import request
from urllib.parse import quote
import hmac
import odoo

_logger = logging.getLogger(__name__)


class AliPayLogin(Home, http.Controller):

    @http.route('/web/alipay/login', type='http', auth='public', website=True, sitemap=False)
    def web_alipay_login(self, *args, **kw):
        """
        支付宝扫码、账号登录
        """
        # 拼接url
        url = request.env['alipay.system.conf'].sudo().search([('key', '=', 'oauth2_url')]).value
        alipay_appid = request.env['ir.config_parameter'].sudo().get_param('alipay.alipay_appid')
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

