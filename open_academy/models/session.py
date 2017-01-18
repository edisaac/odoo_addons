from openerp import models, fields, api, exceptions
from datetime import timedelta


class OpenAcademySession(models.Model):
    _name = "openacademy.session"

    name = fields.Char(string="Name", size=64, requiered=True)
    seats = fields.Integer(string="Seats")
    duration = fields.Float(string="Duration")
    start_date = fields.Date(string="Star Date", default=fields.Date.today)

    course_id = fields.Many2one("openacademy.course", string="Course")
    attendee_ids = fields.One2many("openacademy.attendee", 'session_id', string='attendees')
    instructor_id = fields.Many2one("res.partner", string='Instructor',
                                    domain=['|',
                                            ('is_instructor', '=', True),
                                            ('category_id.name', 'in', ['Instructor 1', 'Instructor 2'])
                                            ])

    remaining_seats = fields.Float(string="Remaining Seats", compute='_remaining_seats')
    active = fields.Boolean(string='Active', default=True)
    attendee_count = fields.Integer(string="Total attendees", compute='_attendee_count')
    end_date = fields.Date(string="End Date", compute='_end_date', inverse='_set_end_date')

    @api.one
    @api.depends('attendee_ids', 'seats')
    def _remaining_seats(self):
        if self.seats == 0:
            self.remaining_seats = 0
        else:
            self.remaining_seats = (1 - (len(self.attendee_ids) / float(self.seats))) * 100

    @api.onchange('seats')
    def _onchange_seats(self):
        res = {}
        if self.seats < 0:
            res['warning'] = {'tittle': 'incorrect value',
                              'message': 'the seats must be more then 0'}

        return res

    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor(self):
        for attendee in self.attendee_ids:
            if attendee.partner_id == self.instructor_id:
                raise exceptions.ValidationError("The Partner and instructor mus be different")

    @api.one
    @api.constrains('seats', 'attendee_ids')
    def _check_attendees(self):
        if self.seats < len(self.attendee_ids):
            raise exceptions.ValidationError("Can not be more attendees than seats")

    @api.one
    @api.depends('attendee_ids')
    def _attendee_count(self):
        self.attendee_count = len(self.attendee_ids)

    @api.one
    @api.depends('start_date', 'duration')
    def _end_date(self):
        start_date = fields.Datetime.from_string(self.start_date)
        duration = timedelta(days=self.duration - 1)
        self.end_date = start_date + duration

    @api.one
    def _set_end_date(self):
        start_date = fields.Datetime.from_string(self.start_date)
        end_date = fields.Datetime.from_string(self.end_date)
        duration = end_date - start_date
        self.duration = duration.days + 1
