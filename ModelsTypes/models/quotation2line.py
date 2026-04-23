from pycparser.c_ast import Default
from xlsxwriter.contenttypes import defaults

from odoo import models,fields,api



class Quotation(models.Model):
    _name = 'quotation.line'
    quotation_id= fields.Many2one('qb.quotation', string='Quotation',
    ondelete='cascade',
    required=True)
    name = fields.Char(required=True)
    qty = fields.Float(required=True)
    unit_price = fields.Float(required=True)
    discount_type = fields.Selection([
        ('percent','Percent'),
        ('fixed','Fixed')
    ],default='fixed',required=True)
    discount_value = fields.Float()
    tax_percent = fields.Float()
    sequence =fields.Integer()
    price_before_discount = fields.Float(compute='_compute_price_before_discount',store=True)
    discount_amount = fields.Float(compute='_compute_discount_amount',store=True)
    price_subtotal =fields.Float(compute='_compute_price_subtotal',store=True)
    tax_amount = fields.Float(compute='_compute_tax_amount',store=True)
    price_total =fields.Float(compute='_compute_price_total',store=True)

    @api.depends('qty','unit_price')
    def _compute_price_before_discount(self):
        for line in self:
            line.price_before_discount = line.qty*line.unit_price

    @api.depends('discount_type','discount_value','price_before_discount')
    def _compute_discount_amount(self):
        for line in self:
            if line.discount_type == 'percent':
                line.discount_amount =  line.price_before_discount * (line.discount_value/100)
            elif line.discount_type == 'fixed' and line.discount_value < line.price_before_discount:
                line.discount_amount = line.discount_value

    @api.depends('discount_amount','price_before_discount')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_before_discount - line.discount_amount
    @api.depends('price_subtotal','tax_percent')
    def _compute_tax_amount(self):
        for line in self:
            line.tax_amount = line.price_subtotal * line.tax_percent/100
    @api.depends('price_subtotal','tax_amount')
    def _compute_price_total(self):
        for line in self:
            line.price_total = line.price_subtotal + line.tax_amount

    @api.onchange('qty','unit_price')
    def _onchange_qty(self):
        for line in self:
            if line.qty < 0:
                line.qty = 1
                line.unit_price = 0
            elif line.unit_price < 0:
                line.qty = 1
                line.unit_price = 0
    @api.onchange('discount_type')
    def _onchange_discount_type(self):
        for line in self:
            line.discount_value = 0.0



