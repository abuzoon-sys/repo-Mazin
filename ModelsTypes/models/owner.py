from odoo import models,fields,api



class Owner(models.Model):
    _name = 'owner'
    name = fields.Char(required=1)
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many(comodel_name='property',inverse_name='owner_id')