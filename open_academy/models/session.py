from openerp import models, fields, api


class OpenAcademySession(models.Model):
    _name = "openacademy.session"

    name = fields.Char("Name", size=64, requiered=True)
    seats = fields.Integer("Seats")
    duration = fields.Float("Duration")
    star_date = fields.Date("Star_Date")
    course_id = fields.Many2one("openacademy.course", string="Course")
    attendee_ids = fields.One2many("openacademy.attendee", 'session_id', string='attendees')
    instructor_id = fields.Many2one("res.partner", string='Instructor')
