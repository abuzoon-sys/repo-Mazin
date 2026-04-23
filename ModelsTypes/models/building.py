from pyexpat.errors import messages

from odoo import models,fields,api



class Building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit =['mail.thread','mail.activity.mixin']
    #_rec_name = 'code' # address name from other fields

    name = fields.Char()
    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)
