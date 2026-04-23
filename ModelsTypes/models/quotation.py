from odoo import models,fields,api



class Quotation(models.Model):
    _name = 'qb.quotation'
    name = fields.Char()
    quotation_number = fields.Char()
    customer_name = fields.Char()
    date =fields.Date()
    state =fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled')
    ],default='draft',required=True)

    currency_symbol = fields.Char(default= 'SAR', readonly=True)
    amount_untaxed = fields.Float(compute='_compute_amount_untaxed',store=True)
    amount_discount = fields.Float(compute='_compute_amount_discount',store=True)
    amount_after_discount = fields.Float(compute='_compute_amount_after_discount',store=True)
    amount_tax = fields.Float(compute='_compute_amount_tax',store=True)
    amount_total = fields.Float(compute='_compute_amount_total',store=True)

    line_ids = fields.One2many(
        comodel_name='quotation.line',
        inverse_name='quotation_id',
        string='Quotation Lines')

    @api.depends(
        'line_ids.price_before_discount',
        'line_ids.discount_amount',
        'line_ids.price_subtotal',
        'line_ids.tax_amount',
        'line_ids.price_total',
    )
    def _compute_amounts(self):
        for rec in self:
            lines = rec.line_ids
            rec.amount_untaxed = sum(lines.mapped('price_before_discount'))
            rec.amount_discount = sum(lines.mapped('discount_amount'))
            rec.amount_after_discount = sum(lines.mapped('price_subtotal'))
            rec.amount_tax = sum(lines.mapped('tax_amount'))
            rec.amount_total = sum(lines.mapped('price_total'))

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
