# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from datetime import datetime, timedelta


class depose(models.TransientModel):
    _name = 'create.depose'

    date_depot = fields.Date(
        string='date_depot', default=fields.Date.today,
        required=False)
    parent_id = fields.Many2one(
        comodel_name='cheque',
        string='Parent_id',
        required=False,

    )

    @api.multi
    def create_date_depot(self):
        self.parent_id.date_depot_form = self.date_depot
        # date_1 = datetime.strptime(self.date_depot, "%Y-%m-%d")
        week = datetime.today().weekday()

        if (week == 5):
            date1 = self.date_depot + timedelta(days=+4)

            self.parent_id.date_a = date1
        elif (week ==6):
            date1 = self.date_depot + timedelta(days=+3)

            self.parent_id.date_a = date1


        else:
            date1 = self.date_depot + timedelta(days=+2)

            self.parent_id.date_a = date1

        self.parent_id.depot()




