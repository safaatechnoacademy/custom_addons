# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectSale(http.Controller):
#     @http.route('/project_sale/project_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_sale/project_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_sale.listing', {
#             'root': '/project_sale/project_sale',
#             'objects': http.request.env['project_sale.project_sale'].search([]),
#         })

#     @http.route('/project_sale/project_sale/objects/<model("project_sale.project_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_sale.object', {
#             'object': obj
#         })
