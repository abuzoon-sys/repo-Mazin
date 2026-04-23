from odoo import models,fields,api



class Order(models.Model):
    _name = 'customer.order'
    customer = fields.Char('custom')
    order_name = fields.Char()
    description = fields.Char()
    location = fields.Char()
    quantity = fields.Integer()

