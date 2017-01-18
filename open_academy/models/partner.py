from openerp import models, fields, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    #fields
    is_instructor = fields.Boolean(string='Instructor')
    session_ids = fields.One2many("openacademy.session", 'instructor_id', string='Sessions')
