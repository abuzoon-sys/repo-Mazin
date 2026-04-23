from odoo import models,fields,api



class Employee(models.Model):
    _name = 'employee.model'
    employee_id = fields.Char('Employee ID')
    first_name = fields.Char()
    last_name = fields.Char()
    phone_number = fields.Char()
    birth_date = fields.Date()
    notes = fields.Char()


