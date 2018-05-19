# -*- coding: utf-8 -*-

from lxml import etree
from datetime import timedelta
from odoo import api,fields,exceptions,tools,models, SUPERUSER_ID,_
from odoo.tools.safe_eval import safe_eval


class ResportSession(models.Model):
    _name = 'session.report'
    _auto = False


    name = fields.Char('Order Reference', readonly=True)
    date = fields.Datetime('Date Order', readonly=True)
    session_id = fields.Many2one('openacamedy.session')
    responsable_id = fields.Many2one('res.users', string='Responsable',readonly=True)
    nbr_seats = fields.Integer(string='Number seats',readonly=True)
    taken_seats = fields.Float(string='Porcentage',readonly=True)
    end_date = fields.Date(string="End Date",readonly=True)
    nbr_participant = fields.Integer(string="Nbr participant",readonly=True)


    def _select(self):
        select_str = """
             SELECT nbr_seats as nbr
        """
        return select_str
    def _from(self):
        from_str = """
                openacademy_session
        """
        return from_str

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
             %s
             FROM ( %s )
             )""" % (self._table, self._select(), self._from(),))
