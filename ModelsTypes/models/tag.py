from odoo import models,fields,api



class Tag(models.Model):
    _name = 'tag'
    name = fields.Char(required=1)
