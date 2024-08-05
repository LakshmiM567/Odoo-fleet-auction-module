# -*- coding: utf-8 -*-
{
    'name': "Fleet Auction",
    'version': "17.0.3.0.0",
    'category': "Fleet",
    'summary': "Fleet Auction",
    'sequence': '8',
    'description': "Fleet Auction",
    'author': "Lakshmi",
    'depends': ['base', 'fleet', 'mail', 'sales_team'],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_auction_views.xml',
        'views/bid_auction_views.xml',
        'data/sequence.xml',
    ],
    'application': True,
    'license': "LGPL-3",
}
