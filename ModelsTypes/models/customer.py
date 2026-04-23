from odoo import models,fields,api



class Customer(models.Model):
    _name = 'customer.customer'
    Customer_ID = fields.Char()
    country = fields.Char()
    city = fields.Char()
    postal_code = fields.Char()




