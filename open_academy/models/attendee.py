from openerp import models, fields, api


class OpenAcademyAttendee(models.Model):
    _name = 'openacademy.attendee'

    name = fields.Char("Name", size=64, requiered=True)
    session_id = fields.Many2one("openacademy.session", string="Session")
    partner_id = fields.Many2one("res.partner", string='Partner')