# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    #
    # def _default_session(self):
    #     session = self.env['openacademy.session'].browse(self._context.get('active_id'))
    #     print('===',session)
    #     return session

    session_id = fields.Many2one('openacademy.session', string="Session")
    attendre_ids = fields.Many2many('res.partner', string="Attendre")

    @api.multi
    def saveattendre(self):
        for r in self:
            r.session_id.participant_ids |= self.attendre_ids

