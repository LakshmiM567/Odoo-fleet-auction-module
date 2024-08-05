# -*- coding: utf-8 -*-
from odoo import fields, models


class BidAuction(models.Model):
    _name = "bid.auction"
    _description = "Bid Auction"
    _rec_name = "auction_id"
    _inherit = "mail.thread"

    auction_id = fields.Many2one('fleet.auction',
                                 string="Auction ID", required=True)
    company_id = fields.Many2one(
        'res.company', store=True, copy=False,
        string="Company", default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one(
        'res.currency', string="Currency",
        related='company_id.currency_id',
        default=lambda self: self.env.user.currency_id.id)
    amount = fields.Float(string="Bid Amount", currency_field='currency_id')
    price = fields.Float(
        string="Bid Price", currency_field='currency_id',
        related='auction_id.start_price')
    date = fields.Date(string="Bid Date", default=fields.Date.today())
    customer_id = fields.Many2one('res.partner', string="Customer")
    phone_number = fields.Char(string="Phone No.", related='customer_id.phone')
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed')],
        required=True, default='draft', tracking=True)
    winner = fields.Boolean(string="Winner", default=False, readonly=True)
