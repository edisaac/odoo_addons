from openerp import models, fields, api


class OpenAcademyCourse(models.Model):
    _name = "openacademy.course"

    name = fields.Char("Name", size=32, required=True)
    description = fields.Text("Description")
    session_ids = fields.One2many("openacademy.session", 'course_id', string='sessions')

    #python-chart pydot pyparsing pyd usb>=1.0.0b1