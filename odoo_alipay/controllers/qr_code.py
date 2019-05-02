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


class AliPayPrecreateQrCode(Home, http.Controller):

    @http.route('/web/precreate/open_qr_code', type='http', auth='user', website=True, sitemap=False)
    def web_precreate_qr_code(self, *args, **kw):
        """
        打开二维码图片
        :param args:
        :param kw:
        :return:
        """
        print("------")
        values = request.params.copy()
        return request.render('odoo_alipay.qr_code_view', values)

