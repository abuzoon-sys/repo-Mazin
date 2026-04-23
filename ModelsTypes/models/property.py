from pyexpat.errors import messages

from pyparsing import actions

from odoo import models,fields,api



class Property(models.Model):
    _name = 'property'
    name = fields.Char()
    ref = fields.Char(default='New',readonly=True)
    description = fields.Text()
    postcode = fields.Char()
    data_availability = fields.Date()
    expected_selling_date = fields.Date()
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff= fields.Float(compute='_compute_diff',store=True)
    bedrooms = fields.Integer()
    livining_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area =fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address',readonly=0)
    owner_phone = fields.Char(related='owner_id.phone',readonly=0)
    line_ids = fields.One2many('property.line','property_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Solded'),
        ('closed', 'Closed'),
    ]  ,default='draft')

    _sql_constraints = [(
        'name_unique','unique("name")','This name is exist'
    )] #this is code for repeating the name

    @api.depends('expected_price','selling_price','owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print('Compute Success ')
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def onchange_expected_price(self):
        for rec in self:
            print('Compute Expected Price')
            if rec.expected_price:
                rec.expected_price != -rec.expected_price
            return {
                'warning': {'title':'warning','message':'ronge value','type':'notification'}
            }


    def action_draft(self):
        for rec in self:
            rec.state='draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state,'pending')
            rec.state='pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state='sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'
    def create_history_record(self,old_state,new_state,reason=None):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason':reason or '',
            })

    def action_open_change_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('ModelsTypes.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('ModelsTypes.owner_action')
        view_id = self.env.ref('ModelsTypes.owner_view_form').id
        action['res_id']=self.owner_id.id
        action['views']=[[view_id,'form']]
        return action

    def check_expected_selling_date(self):
        property_id = self.search([])
        for rec in property_id:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True
    def action(self):
        print(self.env['owner'].search([]))

    @api.model
    def create(self,vals):
        res = super(Property,self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res




class PropertyLine(models.Model):
    _name = 'property.line'
    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Text()
