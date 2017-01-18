from openerp import models, fields, api


class OpenAcademyCourse(models.Model):
    _name = "openacademy.course"

    name = fields.Char(string="Name", size=32, required=True)
    description = fields.Text(string="Description")
    session_ids = fields.One2many("openacademy.session", 'course_id', string='sessions')
    responsible_id = fields.Many2one("res.users", string='Responsible')
    _sql_constraints = [('name_description_ck',
                         'CHECK(name!=description)',
                         'name and description must be different'),
                        ('name_unique', 'unique (name)', 'name must be unique')
                        ]

    #sobrescribiendo el metodo copy
    @api.one
    def copy(self, default=None):
        default['name']=self.name + '(copy)'
        return super(OpenAcademyCourse, self).copy(default)

    #python-chart pydot pyparsing pyd usb>=1.0.0b1

    # sobrescribiendo el metodo name que muestra los datos de una lista
    @api.multi
    def name_get(self, default=None):
        # res = super(OpenAcademicCourse, self).name_get()
        res = []
        for course in self:
            t = (course.id, "%s %s" % (course.name, course.responsible_id
                                       and "(%s)" % course.responsible_id.name or ""))
            res.append(t)

        return res
