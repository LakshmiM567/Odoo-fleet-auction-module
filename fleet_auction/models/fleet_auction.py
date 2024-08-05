# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FleetAuction(models.Model):
    _name = "fleet.auction"
    _description = "Fleet Auction"
    _inherit = "mail.thread"

    fleet_ids = fields.One2many('bid.auction',
                                'auction_id', string="Bid",
                                domain="[('status','=','confirmed')]")

    name = fields.Char(string="Name", copy=False)
    vehicle_name_id = fields.Many2one('fleet.vehicle',
                                      string="Vehicle Name", required=True)
    brand_id = fields.Many2one(string="Brand",
                               related="vehicle_name_id.brand_id")
    start_date = fields.Date(string="Start Date", default=fields.Date.today())
    end_date = fields.Date(string="End Date", default=fields.Date.today())

    responsible_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user, string="Responsible")
    active = fields.Boolean(string="Active", default=True)
    description = fields.Html(string="Description")
    image = fields.Binary(string="")
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                   ('ongoing', 'Ongoing'), ('success', 'Success'),
                   ('cancelled', 'Cancelled')],
        required=True, tracking=True, default='draft')
    company_id = fields.Many2one(
        'res.company', store=True, copy=False,
        string="Company", default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one(
        'res.currency', string="Currency",
        related='company_id.currency_id',
        default=lambda self: self.env.user.company_id.currency_id.id)
    start_price = fields.Float(
        string="Start Price", currency_field='currency_id', copy=False)
    won_price = fields.Float(
        string="Won Price", currency_field='currency_id', copy=False,
        readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string="Customer", readonly=True)
    phone = fields.Char(
        string="Phone", related='partner_id.phone')
    email = fields.Char(
        string="Email", related='partner_id.email')
    tags = fields.Many2many('crm.tag', string="Tags")
    bid_count = fields.Integer(string="Bids",
                               compute='compute_bid_count',
                               default=0)

    @api.constrains('start_date', 'end_date')
    def _check_start_date(self):
        """to ensure start date precedes the end date"""
        if self.start_date > self.end_date:
            raise ValidationError('Start date must precede the end date')

    def button_confirm(self):
        self.state = "confirmed"

    def button_cancel(self):
        self.state = "cancelled"
        # print(self.partner_id.country_id.currency_id.name)

    def button_end(self):
        self.state = "success"

    @api.model_create_multi
    def create(self, vals):
        """to generate unique sequence for records in the name field"""
        # print(vals, self)
        vals[0]['name'] = \
            (self.env['ir.sequence'].next_by_code('my_sequence_code'))
        return super(FleetAuction, self).create(vals)

    def compute_bid_count(self):
        """to compute the total count of bids under the auction"""
        for record in self:
            record.bid_count = self.env['bid.auction'].search_count(
                [('auction_id', '=', self.id)])

    def action_get_bid_record(self):
        """to get the records of total bids"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bids',
            'view_mode': 'tree',
            'res_model': 'bid.auction',
            'domain': [('auction_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_stop(self):
        """to find the highest bid and update customer and won amount"""
        bids = self.env['bid.auction'].search([('auction_id', '=', self.id)])
        # print("string", bids)
        if bids:
            highest_bid = max(bids, key=lambda k: k.amount)
            highest_bid.winner = True
            self.partner_id = highest_bid.customer_id
            self.won_price = highest_bid.amount
