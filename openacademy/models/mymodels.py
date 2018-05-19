# -*- coding: utf-8 -*-

from lxml import etree
from datetime import timedelta
from odoo import api,fields,exceptions,tools,models, SUPERUSER_ID,_
from odoo.tools.safe_eval import safe_eval


class Cours(models.Model):
    _name = 'openacademy.course'


    name = fields.Char(string='Name',help="c'est le nom du cours")
    description = fields.Text(string='Déscription')
    date_debut = fields.Date(date='Date début', readonly=True)
    active = fields.Boolean('Active', default=True)
    responsable_id=fields.Many2one('res.users',string='Résponsable')
    session_ids=fields.One2many('openacademy.session','cours_id',string='Sessions')
    cours_state =fields.Selection([
        ('start','en cours'),
        ('end','termine')
    ],string='etat',default='start')

    _sql_constraints=[('verif_cours','CHECK(name != description)',"name  different de la description"),
                      ('unique_name','UNIQUE(name)',"name doit etre unique"),]

    @api.multi
    def change_etat(self):
        for r in self:
           r.write({'cours_state':'end'})



class Session(models.Model):
    _name = 'openacademy.session'
    _inherit =['mail.alias.mixin','mail.thread','portal.mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']


    def _default_cours(self):
        cours=self.env['openacademy.course'].search([('name','=' ,'math')])
        print("===========",cours)
        cour = cours[0]
        print('*****************',cour)
        return cour

    name = fields.Char(string='Name', track_visibility='always',required=True ,)
    date_start = fields.Date(string='Date start',default=fields.Date.today)
    duration=fields.Float(string='Durée')
    seats=fields.Integer(string='Nombre de place 1')
    maitre_id=fields.Many2one('res.partner',setring='Maitre',domain=[('student' , '=' , True)])
    cours_id=fields.Many2one('openacademy.course',string='Cours',default=_default_cours)
    participant_ids=fields.Many2many('res.partner',string='Participant')
    nbr_seats=fields.Integer(string='Number seats')
    taken_seats=fields.Float(string='Porcentage',compute="_porcentage")
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date')
    nbr_participant=fields.Integer(string="Nbr participant",compute="_nbrparticipant")
    color=fields.Integer(string="color")
    state=fields.Selection([
        ('brouillon','Brouillon'),
        ('confirme','Confirmé'),
        ('termine','Terminé'),
            ],string='state',track_visibility='onchange',default='brouillon',)

    @api.multi
    def action_brouillon(self):
       self.state='brouillon'

    @api.multi
    def action_confirme(self):
            self.state = 'confirme'

    @api.multi
    def action_termine(self):
        self.state = 'termine'

    @api.multi
    def ajout_participant(self):
            vue=self.env.ref('openacademy.view_wizard_form')
            print('=====',vue)
            return {
                    'name':'participant',
                    'type': 'ir.actions.act_window',
                    'res_model' : 'openacademy.wizard',
                    'view_id' : vue.id,
                    'view_mode' : 'form',
                    'view_type': 'form',
                    'target': 'new',

                }


    @api.depends("participant_ids")
    def _nbrparticipant(self):
        for r in self:
            r.nbr_participant=len(r.participant_ids)



    @api.depends("date_start", "duration")
    def _get_end_date(self):
        for r in self:
            if not (r.date_start and r.duration):
                r.end_date = r.date_start
                continue
            date_start = fields.Datetime.from_string(r.date_start)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = date_start  + duration



    @api.depends("nbr_seats","participant_ids")
    def _porcentage(self):
        for r in self:
            if not r.nbr_seats:
                r.taken_seats=0.0
            else:
                r.taken_seats=100.0 * len(r.participant_ids)/r.nbr_seats

    @api.onchange("nbr_seats","participant_ids")
    def _valid(self):
        if self.nbr_seats<0:
            return {
                'warning':{
                    'title':"Valeur negatif",
                    'message':"valeur invalide",
                },

            }
        if self.nbr_seats<len(self.participant_ids):
            return {
                'warning':{
                    'title':"Alert",
                    'message':"nbr place inferieur nbr participant",
                },
            }

    @api.constrains('maitre_id=','participant_ids')
    def _cont(selfs):
        for r in selfs:
            if r.maitre_id in r.participant_ids:
                raise exceptions.ValidationError("Le maitre est parmi les participants")



class OpenacademyPartner(models.Model):
    _inherit='res.partner'


    session_ids=fields.Many2many('openacademy.session',string='Session')
    responsable_id=fields.Many2one('res.users',string='résponsable')
    student=fields.Boolean(string='est un étuddiant')

class Test(models.Model):
    _name = 'openacademy.test'


    name = fields.Char(string='Name' , required=True)
    designation = fields.Date(string='Désignation')
    maitre_id=fields.Many2one('res.partner',setring='Maitre',domain=[('student' , '=' , True)])
    cours_id=fields.Many2one('openacademy.course',string='Cours')
    participant_ids=fields.Many2many('res.partner',string='Participant')
