# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
from datetime import datetime
from datetime import datetime, timedelta

from babel.dates import format_datetime, format_date


class chek(models.Model):
    _name = 'cheque'
    _rec_name = 'sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    benifiaiere = fields.Char(
        string='Bénéficiaire',
        required=True,track_visibility='onchange',)
    sequence = fields.Char(string="sequence", default='New', readonly=True)

    ville = fields.Char(
        string='Ville',
        required=False,track_visibility='onchange')
    date_echeace = fields.Date(
        string='Date Échéance',
        required=True,track_visibility='onchange')
    proprietaire = fields.Char(
        string='propriétaire',
        required=False,track_visibility='onchange')
    mantant = fields.Integer(
        string='Montant',
        required=False,track_visibility='onchange')
    Nemero = fields.Integer(
        string='Numero',
        required=True,track_visibility='onchange')
    state = fields.Selection(
        string='State',
        selection=[('brouillon', 'brouillon'),
                   ('cheque_a_lencaissent', 'chèque à l encaissement'),
                   ('deposé', 'dépose'),
                   ('encaissé', 'encaissé'),
                   ('in_payé', 'in payé'),
                   ],
        default="brouillon",
        track_visibility='onchange',
        )
    in_cheque = fields.Boolean(
        string=' in_cheque',track_visibility='onchange',
        required=False)
    date_depot_form = fields.Date(
        string='Date dépôt',track_visibility='onchange',
        required=False,store=True,readonly='1' )

    type = fields.Selection(
        string='Type',
        selection=[('Endossable', 'Endossable'),
                   ('non_endossable', 'Non Endossable'), ],
        required=True,track_visibility='onchange' ,)

    @api.model
    def create(self, vals):
        result = super(chek, self).create(vals)

        result.sequence = self.env['ir.sequence'].next_by_code('bureau.cheque')

        return result

    def valider(self):

        if self.create_uid.id:
            user_id = self.create_uid.id
            ext = self.env.ref('IA_gestion_cheque.model_cheque').id
            self.activity_ids.create(
                {'activity_type_id': 4, 'res_id': self.id, 'user_id': user_id,
                 'res_model_id': ext,
                 'date_deadline': self.date_echeace,
                 'note': 'le cheque valider'
                 })
        self.state ='cheque_a_lencaissent'
    def valider_payer(self):
        if self.create_uid.id:
            user_id = self.create_uid.id
            ext = self.env.ref('IA_gestion_cheque.model_cheque').id
            self.activity_ids.create(
                {'activity_type_id': 4, 'res_id': self.id, 'user_id': user_id,
                 'res_model_id': ext,
                 'date_deadline': self.date_echeace,
                 'note': 'le cheque valider'
                 })
        self.state ='cheque_a_lencaissent'





    def depot(self):

        user_id = self.create_uid.id
        ext = self.env.ref('IA_gestion_cheque.model_cheque').id
        self.activity_ids.create(
                {'activity_type_id': 4, 'res_id': self.id, 'user_id': user_id,
                 'res_model_id': ext,
                 'date_deadline': self.date_a,
                 'note': 'cheque deposé'
                 })







    def creat_wizart(self):
        # date_1 = datetime.strptime(self.date_depot_form, "%Y-%m-%d")
        # week = datetime.today().weekday()
        #
        # # if (week == 5):
        # date1 = date_1 + timedelta(days=+2)
        # print(date1)
        # self.date_a = date1
         self.state ='deposé'

         return {
            'name': 'Confirmation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.depose',
            'context': {'default_parent_id': self.id},
            'view_id': False,
            'target': 'new',
            'nodestroy': True,
        }

    def cheque_encaisement_payer(self):
        self.state ='encaissé'
    def paye_payer(self):
        self.state = 'in_payé'
    def cheque_encaisement(self):
        self.state ='encaissé'
    def paye(self):
        self.state = 'in_payé'

    def envoiye(self):

            template_values = {
                'email_from': self.create_uid.email,
                'email_to': self.create_uid.email,
                'email_cc': False,
                'partner_to': False,
                'scheduled_date': False,
            }
            template = self.env.ref('ia_bureau_order.email_template')
            template.write(template_values)
            with self.env.cr.savepoint():
                template.send_mail(self.id, force_send=True, raise_exception=True)
    date_a = fields.Date(
        string='Date_a',
        required=False)


    # @api.onchange('date_a')
    # def week_depot(self):
    #
    #     # my_date = date.today()
    #     if self.date_depot_form:
    #         today = fields.Datetime.now(self)
    #         week = datetime.today().weekday()
    #
    #         date_1 = datetime.strptime(self.date_depot_form, "%Y-%m-%d")
    #
    #         #
    #         # first_day_of_week = today + timedelta(days=-day_of_week + 1)
    #
    #         print(week)
    #         if (week == 5) :
    #
    #             date1 = date_1 + timedelta(days=+2)
    #             print(date1)
    #             self.date_a = date1
















