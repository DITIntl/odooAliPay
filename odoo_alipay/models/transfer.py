# -*- coding: utf-8 -*-
import datetime
import json
import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipayFundTransToaccountTransferRequest import AlipayFundTransToaccountTransferRequest
from alipay.aop.api.domain.AlipayFundTransToaccountTransferModel import AlipayFundTransToaccountTransferModel
from odoo import fields, models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AliPayTransfer(models.Model):
    _date_name = '支付宝转账'
    _name = 'alipay.transfer'
    _inherit = ['mail.thread']
    _rec_name = 'out_biz_no'

    PAYEETYPE = [
        ('ALIPAY_USERID', '用户号'),
        ('ALIPAY_LOGONID', '邮箱和手机号')
    ]
    out_biz_no = fields.Char(string='订单编号')
    payee_type = fields.Selection(string=u'收款方账户类型', selection=PAYEETYPE, default='ALIPAY_LOGONID')
    payee_account = fields.Many2one(comodel_name='res.partner', string=u'收款账户',
                                    domain=[('alipay_account', '!=', ''), ('alipay_user_id', '!=', '')])
    amount = fields.Float(string=u'转账金额', digits=(13, 2), default=0.0)
    payer_show_name = fields.Char(string='付款方名称')
    payee_real_name = fields.Char(string='收款方真实姓名')
    remark = fields.Text(string=u'转账备注')
    company_id = fields.Many2one(comodel_name='res.company', string=u'公司',
                                 default=lambda self: self.env.user.company_id.id)
    state = fields.Selection(string=u'状态', selection=[('00', '草稿'), ('01', '待确认'), ('02', '成功'), ('03', '失败')],
                             default='00')
    pay_date = fields.Datetime(string=u'支付时间')
    order_id = fields.Char(string=u'支付宝转账单据号')

    _sql_constraints = [
        ('out_biz_no_uniq', 'unique(out_biz_no)', u'订单编号不允许重复!'),
    ]

    @api.model
    def create(self, values):
        values['out_biz_no'] = self.env['ir.sequence'].sudo().next_by_code('alipay.transfer.code')
        return super(AliPayTransfer, self).create(values)

    @api.onchange('payee_account')
    def onchange_payee_account(self):
        if self.payee_account:
            self.payee_real_name = self.payee_account.alipay_real_name

    @api.multi
    def summit_transfer(self):
        """
        转账功能函数
        :return:
        """
        for res in self:
            alipay_client_config = AlipayClientConfig()
            alipay_client_config.server_url = self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_gateway')
            alipay_client_config.app_id = self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_appid')
            alipay_client_config.encrypt_key = self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_aes')
            alipay_client_config.app_private_key = self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_sign')
            alipay_client_config.alipay_public_key = self.env['ir.config_parameter'].sudo().get_param('odoo_alipay.alipay_public_key')
            client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

            transfer_model = AlipayFundTransToaccountTransferModel()
            transfer_model.out_biz_no = res.out_biz_no  # 编号
            transfer_model.payee_type = res.payee_type  # 收款方账户类型
            if res.payee_type == 'ALIPAY_USERID':
                transfer_model.payee_account = res.payee_account.alipay_user_id  # 收款账户(用户号)
            else:
                transfer_model.payee_account = res.payee_account.alipay_account  # 收款账户（账号）
            transfer_model.amount = str(res.amount)  # 转账金额
            transfer_model.payer_show_name = res.payer_show_name if res.payer_show_name else ''  # 付款方姓名
            transfer_model.payee_real_name = res.payee_real_name if res.payee_real_name else '' # 收款方真实姓名
            transfer_model.remark = res.remark if res.remark else ''  # 转账备注

            transfer_request = AlipayFundTransToaccountTransferRequest(transfer_model)
            result = client.execute(transfer_request)
            logging.info(">>>支付宝转账结果:{}".format(result))
            result = json.loads(result, 'utf-8')
            if result.get('code') != '10000':
                raise UserError("转账失败！原因为:{}".format(result.get('sub_msg')))
            elif result.get('code') == '10000':
                res.write({'state': '02', 'pay_date': datetime.datetime.now(), 'order_id': result.get('order_id')})
                res.message_post(body=result.get('msg'), message_type='notification')
            else:
                res.write({'state': '01'})
                res.message_post(body="操作失败！请使用查询功能", message_type='notification')

