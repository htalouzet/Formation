# -*- coding: utf-8 -*-
from odoo import http

# class Extra-addons/openacademy(http.Controller):
#     @http.route('/extra-addons/openacademy/extra-addons/openacademy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extra-addons/openacademy/extra-addons/openacademy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('extra-addons/openacademy.listing', {
#             'root': '/extra-addons/openacademy/extra-addons/openacademy',
#             'objects': http.request.env['extra-addons/openacademy.extra-addons/openacademy'].search([]),
#         })

#     @http.route('/extra-addons/openacademy/extra-addons/openacademy/objects/<model("extra-addons/openacademy.extra-addons/openacademy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extra-addons/openacademy.object', {
#             'object': obj
#         })