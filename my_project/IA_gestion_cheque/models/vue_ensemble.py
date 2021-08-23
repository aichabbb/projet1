import logging
_logger = logging.getLogger(__name__)

import json
from datetime import datetime, timedelta

from babel.dates import format_datetime, format_date

from odoo import models, api, _, fields
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, safe_eval


class vueEmissionReception(models.Model):
    _name = 'kanban'

    nom = fields.Char(
        string='Nom',
        required=False)

    color = fields.Integer("Color Index", default=0)

    is_payer = fields.Boolean(
        string='Is_emmision',
        required=False)
    is_recu = fields.Boolean(
        string='Is_repssion',
        required=False)

    nbr_cheque_val = fields.Integer(compute='nombre_cheque_valider')

    @api.depends('nbr_cheque_val')
    def nombre_cheque_valider(self):
        for record in self:
            nombre_cheque_valider = self.env['cheque'].search_count(
                [('state', '=', 'cheque_a_lencaissent'),('in_cheque', '=', False)])
            record.nbr_cheque_val = nombre_cheque_valider

    nbr_cheque_lencaissent = fields.Integer(compute='nombre_cheque_lencaisement')

    @api.depends('nbr_cheque_lencaissent')
    def nombre_cheque_lencaisement(self):
        for record in self:
            nombre_cheque_encaisement = self.env['cheque'].search_count(
                [('state', '=', 'deposé'),('in_cheque', '=', False)])
            record.nbr_cheque_lencaissent = nombre_cheque_encaisement

    nbr_rc_refuse = fields.Integer(compute='nombre_reception_refuse')

    nbr_cheque_payer_val = fields.Integer(compute='nombre_cheque_payer_valider')

    @api.depends('nbr_cheque_payer_val')
    def nombre_cheque_payer_valider(self):
        for record in self:
            nombre_cheque_payer_valider = self.env['cheque'].search_count(
                [('state', '=', 'cheque_a_lencaissent'), ('in_cheque', '=', True)])
            record.nbr_cheque_payer_val = nombre_cheque_payer_valider

    nbr_cheque_payer_enc = fields.Integer(compute='nombre_cheque_payer_encaiser')

    @api.depends('nbr_cheque_payer_enc')
    def nombre_cheque_payer_encaiser(self):
        for record in self:
            nombre_cheque_payer_encaise = self.env['cheque'].search_count(
                [('state', '=', 'encaissé'), ('in_cheque', '=', True)])
            record.nbr_cheque_payer_enc = nombre_cheque_payer_encaise

    nbr_cheque_recu_bry = fields.Integer(compute='nombre_cheque_recu_bry')

    @api.depends('nbr_cheque_recu_bry')
    def nombre_cheque_recu_bry(self):
        for record in self:
            nombre_cheque_recu_br = self.env['cheque'].search_count(
                [('state', '=', 'brouillon'), ('in_cheque', '=', False)])
            record.nbr_cheque_recu_bry = nombre_cheque_recu_br

    nbr_cheque_payer_br = fields.Integer(compute='nombre_cheque_payer_bry')

    @api.depends('nbr_cheque_payer_br')
    def nombre_cheque_payer_bry(self):
        for record in self:
            nombre_cheque_payer_bry = self.env['cheque'].search_count(
                [('state', '=', 'brouillon'), ('in_cheque', '=', True)])
            record.nbr_cheque_payer_br = nombre_cheque_payer_bry

    nbr_cheque_recu_enc = fields.Integer(compute='nombre_cheque_recu_payer')

    @api.depends('nbr_cheque_recu_enc')
    def nombre_cheque_recu_payer(self):
        for record in self:
            nombre_cheque_recu_encaise = self.env['cheque'].search_count(
                [('state', '=', 'encaissé'), ('in_cheque', '=', False)])

    nbr_cheque_payer_paye = fields.Integer(compute='nombre_cheque_payer_payer')

    @api.depends('nbr_cheque_payer_paye')
    def nombre_cheque_payer_payer(self):
        for record in self:
            nombre_cheque_payer_paye = self.env['cheque'].search_count(
                [('state', '=', 'in_payé'), ('in_cheque', '=', True)])
            record.nbr_cheque_payer_paye = nombre_cheque_payer_paye
    nbr_cheque_recu_paye = fields.Integer(compute='nombre_cheque_recu_payer')

    @api.depends('nbr_cheque_recu_paye')
    def nombre_cheque_recu_payer(self):
        for record in self:
            nombre_cheque_recu_paye = self.env['cheque'].search_count(
                [('state', '=', 'in_payé'), ('in_cheque', '=', False)])
            record.nbr_cheque_recu_paye = nombre_cheque_recu_paye

    # nbr_cheque_lencaissent = fields.Integer(compute='nombre_cheque_lencaisement')

    # @api.depends('nbr_cheque_lencaissent')
    # def nombre_cheque_lencaisement(self):
    #     for record in self:
    #         nombre_cheque_encaisement = self.env['cheque'].search_count(
    #             [('state', '=', 'deposé'), ('in_cheque', '=', False)])
    #         record.nbr_cheque_lencaissent = nombre_cheque_encaisement
    #
    # nbr_rc_refuse = fields.Integer(compute='nombre_reception_refuse')

    @api.depends('nbr_rc_refuse')
    def nombre_reception_refuse(self):
        for record in self:
            nombre_recep_refuse = self.env['bureau.order'].search_count(
                [('state', '=', 'refusé'),('in_reception', '=', True)])
            record.nbr_rc_refuse = nombre_recep_refuse

    nbr_emis_valider = fields.Integer(compute='nombre_emission_valider')

    @api.depends('nbr_emis_valider')
    def nombre_emission_valider(self):
        for record in self:
            emiss_valider = self.env['bureau.order'].search_count(
                [('state_emission', '=', 'valider'), ('in_reception', '=', False)])
            record.nbr_emis_valider = emiss_valider

    nbr_acceser_reseption_e = fields.Integer(compute='nombre_emission_acceser_reseption')

    @api.depends('nbr_acceser_reseption_e')
    def nombre_emission_acceser_reseption(self):
        for record in self:
            emiss_acceser_reseption = self.env['bureau.order'].search_count(
                [('state_emission', '=', 'accese_reeption'), ('in_reception', '=', False)])
            record.nbr_acceser_reseption_e = emiss_acceser_reseption

    nbr_met_br_res = fields.Integer(compute='nombre_mettre_broui')

    @api.depends('nbr_met_br_res')
    def nombre_mettre_broui(self):
        for record in self:
            nbr_mettre_broui = self.env['bureau.order'].search_count(
                [('state_emission', '=', 'Brouillon'), ('in_reception', '=', False)])
            record.nbr_met_br_res = nbr_mettre_broui



    def _graph_title_and_key_2(self):
        return ['', ('Bank: Balance')]







    def _get_bar_graph_select_query(self):

        req = " select count(sequence) as total1  ,min(date_echeace) as date_agg  from cheque b  where   in_cheque = 'false' and state = 'cheque_a_lencaissent' "
        return req

    @api.multi
    def get_bar_graph_datas(self):
        data = []
        today = fields.Datetime.now(self)
        data.append({'label': _('Past'), 'value': 0.0 ,'type': 'past'})
        day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang') or 'en_US'))
        first_day_of_week = today + timedelta(days=-day_of_week + 1)
        for i in range(-1, 4):
            if i == 0:
                label = _('This Week')

            elif i == 3:
                label = _('Future')
            else:
                start_week = first_day_of_week + timedelta(days=i * 7)
                end_week = start_week + timedelta(days=6)
                if start_week.month == end_week.month:
                    label = str(start_week.day) + '-' + str(end_week.day) + ' ' + format_date(end_week, 'MMM',
                                                                                              locale=self._context.get(
                                                                                                  'lang') or 'en_US')
                else:
                    label = format_date(start_week, 'd MMM',
                                        locale=self._context.get('lang') or 'en_US') + '-' + format_date(end_week,
                                                                                                         'd MMM',
                                                                                                         locale=self._context.get(
                                                                                                             'lang') or 'en_US')
            data.append({'label': label, 'value': 0.0, 'type': 'past' if i < 0 else 'future'})

       # Build SQL query to find amount aggregated by week
        (select_sql_clause) = self._get_bar_graph_select_query()

        query = ''
        start_date = (first_day_of_week + timedelta(days=-7))
        for i in range(0, 6):
            if i == 0:
                query += "(" + select_sql_clause + " and date_echeace < '" + start_date.strftime(DF) + "')"
            elif i == 5:
                query += " UNION ALL (" + select_sql_clause + " and date_echeace >= '" + start_date.strftime(DF) + "')"
            else:
                next_date = start_date + timedelta(days=7)
                query += " UNION ALL (" + select_sql_clause + " and date_echeace >= '" + start_date.strftime(
                    DF) + "' and date_echeace < '" + next_date.strftime(DF) + "')"
                start_date = next_date


        self.env.cr.execute(query)

        query_results = self.env.cr.dictfetchall()

        for index in range(0, len(query_results)):
            if query_results[index].get('date_agg') != None:
                data[index]['value'] = query_results[index].get('total1')





        [graph_title, graph_key] = self._graph_title_and_key()
        return [{'values': data, 'title': graph_title, 'key': graph_key}]




    def _graph_title_and_key(self):
         return ['', _(' nombres validé')]


    last_month = fields.Integer(compute='date_f')
    today = fields.Datetime.now()

    @api.depends('last_month')
    def date_f(self):

        for record in self:
            _date = self.env['cheque'].search_count(
                [('date_echeace', '=', record.dat), ('in_cheque', '=', False)])
            record.last_month = _date


    @api.multi
    def valider_cheque_recu(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_tree').id
        return {
            'name': ('cheque_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', False), ('state', '=', 'cheque_a_lencaissent')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_form').id, 'form')],

        }

    @api.multi
    def lencaiser_cheque_recu(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_tree').id
        return {
            'name': ('cheque_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', False), ('state', '=', 'deposé')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_form').id, 'form')],

        }

    @api.multi
    def br_cheque_recu(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_tree').id
        return {
            'name': ('cheque_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', False), ('state', '=', 'brouillon')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_form').id, 'form')],

        }
    @api.multi
    def enc_cheque_recu(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_tree').id
        return {
            'name': ('cheque_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', False), ('state', '=', 'encaissé')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_form').id, 'form')],

        }
    @api.multi
    def paye_cheque_recu(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_tree').id
        return {
            'name': ('cheque_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', False), ('state', '=', 'in_payé')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_form').id, 'form')],

        }

    @api.multi
    def paye_cheque_paye(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_payer_tree').id
        return {
            'name': ('cheque_payer_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', True), ('state', '=', 'in_payé')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_payer_form').id, 'form')],

        }

    @api.multi
    def br_cheque_paye(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_payer_tree').id
        return {
            'name': ('cheque_payer_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', True), ('state', '=', 'brouillon')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_payer_form').id, 'form')],

        }
    @api.multi
    def enc_cheque_paye(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_payer_tree').id
        return {
            'name': ('cheque_payer_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', True), ('state', '=', 'encaissé')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_payer_form').id, 'form')],

        }

    @api.multi
    def val_cheque_paye(self):
        view_id = self.env.ref('IA_gestion_cheque.cheque_view_payer_tree').id
        return {
            'name': ('cheque_payer_view_tree'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cheque',
            'domain': [('in_cheque', '=', True), ('state', '=', 'cheque_a_lencaissent')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('IA_gestion_cheque.cheque_view_payer_form').id, 'form')],

        }

    @api.multi
    def approuver_reception(self):
        view_id = self.env.ref('ia_bureau_order.ia_bureau_order_reception_list').id
        return {
            'name': ('liste de reception aprouver'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'bureau.order',
            'domain': [('in_reception', '=', True), ('state', '=', 'approver')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('ia_bureau_order.ia_bureau_order_reception_form').id, 'form')],

        }

    @api.multi
    def refuser_reception(self):
        view_id = self.env.ref('ia_bureau_order.ia_bureau_order_reception_list').id
        return {
            'name': ('liste de reception refesu'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'bureau.order',
            'domain': [('in_reception', '=', True), ('state', '=', 'refusé')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('ia_bureau_order.ia_bureau_order_reception_form').id, 'form')],

        }

    @api.multi
    def valider_emission(self):
        view_id = self.env.ref('ia_bureau_order.ia_bureau_order_list').id
        return {
            'name': ('liste de emission valider'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'bureau.order',
            'domain': [('in_reception', '=', False), ('state_emission', '=', 'valider')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('ia_bureau_order.ia_bureau_order_form').id, 'form')],

        }

    @api.multi
    def accese_reeption_emission(self):
        view_id = self.env.ref('ia_bureau_order.ia_bureau_order_list').id
        return {
            'name': ('liste de emission Accusé de réception'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'bureau.order',
            'domain': [('in_reception', '=', False), ('state_emission', '=', 'accese_reeption')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('ia_bureau_order.ia_bureau_order_form').id, 'form')],

        }

    @api.multi
    def Brouillon_emission(self):
        view_id = self.env.ref('ia_bureau_order.ia_bureau_order_list').id
        return {
            'name': ('liste de emission mettre en Brouillon'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'bureau.order',
            'domain': [('in_reception', '=', False), ('state_emission', '=', 'Brouillon')],
            'view_id': False,
            'views': [(view_id, 'tree'), (self.env.ref('ia_bureau_order.ia_bureau_order_form').id, 'form')],

        }

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_bar_graph_datas_2())

    @api.one
    def _kanban_dashboard_graph(self):
        self.kanban_dashboard_graph = json.dumps(self.get_bar_graph_datas_2())

    kanban_dashboard = fields.Text(compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')

    @api.multi
    def get_bar_graph_datas_2(self):
        data = [{}]

        for i in self:
            if i.nbr_rec_val > 0:
                label = ('valider')
                data.append({'label': label, 'value': i.nbr_rec_val})

            if i.nbr_rec_apr:
                label = ('approuvé')
                data.append({'label': label, 'value': i.nbr_rec_apr})

            if i.nbr_rc_refuse:
                label = ('refusé')
                data.append({'label': label, 'value': i.nbr_rc_refuse})

        return [{'values': data}]

    @api.multi
    def get_bar_graph_datas_1(self):

        data = [{'label': ('past GH'), 'value': 0.0}]

        for i in self:
            if i.last_month:
                data.append({'label': 'past', 'value': i.last_month})
        [graph_title, graph_key] = self._graph_title_and_key_2()
        return [{'values': data, 'title': graph_title, 'key': graph_key}]

    @api.one
    def _kanban_dashboard_1(self):
        self.kanban_dashboard_1 = json.dumps(self.get_bar_graph_datas())

    @api.one
    def _kanban_dashboard_graph_1(self):
        self.kanban_dashboard_graph_1 = json.dumps(self.get_bar_graph_datas())

    kanban_dashboard_1 = fields.Text(compute='_kanban_dashboard_1')
    kanban_dashboard_graph_1 = fields.Text(compute='_kanban_dashboard_graph_1')



    @api.multi
    def get_bar_graph_datas_2_reception(self):
        data = []
        today = fields.Datetime.now(self)
        data.append({'label': _('Past'), 'value': 0.0, 'type': 'past'})
        day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang') or 'en_US'))
        first_day_of_week = today + timedelta(days=-day_of_week + 1)
        for i in range(-1, 4):
            if i == 0:
                label = _('This Week')
            elif i == 3:
                label = _('Future')
            else:
                start_week = first_day_of_week + timedelta(days=i * 7)
                end_week = start_week + timedelta(days=6)
                if start_week.month == end_week.month:
                    label = str(start_week.day) + '-' + str(end_week.day) + ' ' + format_date(end_week, 'MMM',
                                                                                              locale=self._context.get(
                                                                                                  'lang') or 'en_US')
                else:
                    label = format_date(start_week, 'd MMM',
                                        locale=self._context.get('lang') or 'en_US') + '-' + format_date(end_week,
                                                                                                         'd MMM',
                                                                                                         locale=self._context.get(
                                                                                                             'lang') or 'en_US')
            data.append({'label': label, 'value': 0.0, 'type': 'past' if i < 0 else 'future'})

        # Build SQL query to find amount aggregated by week
        (select_sql_clause) = self._get_bar_graph_select_query_reception()

        query = ''
        start_date = (first_day_of_week + timedelta(days=-7))
        for i in range(0, 6):
            if i == 0:
                query += "(" + select_sql_clause + " and date_echeace < '" + start_date.strftime(DF) + "')"
            elif i == 5:
                query += " UNION ALL (" + select_sql_clause + " and date_echeace >= '" + start_date.strftime(DF) + "')"
            else:
                next_date = start_date + timedelta(days=7)
                query += " UNION ALL (" + select_sql_clause + " and date_echeace >= '" + start_date.strftime(
                    DF) + "' and date_echeace < '" + next_date.strftime(DF) + "')"
                start_date = next_date


        self.env.cr.execute(query)

        query_results = self.env.cr.dictfetchall()

        for index in range(0, len(query_results)):
            if query_results[index].get('date_agg') != None:
                data[index]['value'] = query_results[index].get('total1')


        [graph_title, graph_key] = self._graph_title_and_key()
        return [{'values': data, 'title': graph_title, 'key': graph_key}]

    def _get_bar_graph_select_query_reception(self):

        req = " select count(sequence) as total1  ,min(date_echeace) as date_agg  from cheque b  where    in_cheque = 'True' and state = 'cheque_a_lencaissent' "
        return req

    @api.one
    def _kanban_dashboard_reception(self):
        self.kanban_dashboard_reception = json.dumps(self.get_bar_graph_datas_2_reception())

    @api.one
    def _kanban_dashboard_graph_reception(self):
        self.kanban_dashboard_graph_payer = json.dumps(self.get_bar_graph_datas_2_reception())

    kanban_dashboard_reception = fields.Text(compute='_kanban_dashboard_reception')
    kanban_dashboard_graph_payer = fields.Text(compute='_kanban_dashboard_graph_reception')

