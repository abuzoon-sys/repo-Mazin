from odoo import models,fields,api



class Salse(models.Model):
    _name = 'salse.offer'
    name = fields.Char()
    qty = fields.Float()
    unit_price = fields.Float()
    discount_percent = fields.Float()
    discount_amount = fields.Float(compute='_compute_discount_amount', store=True)
    subtotal = fields.Float(compute='_compute_subtotal',store=True)
    tax_precent = fields.Float()
    tax_amount = fields.Float(compute='_compute_tax_amount',store=True)
    total = fields.Float(compute='_compute_total',store=True)
    note = fields.Char()

    @api.depends('qty','unit_price','discount_percent')
    def _compute_discount_amount(self):
        for rec in self:
            rec.discount_amount = rec.qty * rec.unit_price * (rec.discount_percent / 100)

    @api.depends('qty','unit_price','discount_amount')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = (rec.qty * rec.unit_price) - rec.discount_amount

    @api.depends('subtotal','tax_precent')
    def _compute_tax_amount(self):
        for rec in self:
            rec.tax_amount = rec.subtotal * (rec.tax_precent / 100)

    @api.depends('subtotal','tax_amount')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.subtotal + rec.tax_amount

    @api.onchange('discount_percent','note')
    def _onchange_discount_percent(self):
        for rec in self:
            if rec.discount_percent > 50:
                rec.discount_percent = 50
                rec.note = 'Discount capped at 50%'

    @api.onchange('qty','note')
    def _onchange_qty(self):
        for rec in self:
            if rec.qty <= 0:
                rec.qty = 1
                rec.note = 'Quantity must be positive'
