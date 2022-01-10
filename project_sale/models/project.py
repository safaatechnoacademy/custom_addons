
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import api, fields, models, SUPERUSER_ID, _


class ProjectProjectInherit(models.Model):

    _inherit = "project.project"

    sale_order_ids = fields.One2many('sale.order', 'project_id', string="Sales Order #")
    utilized_qty = fields.Float(compute='_calculate_utilized_qty')


    def _calculate_utilized_qty(self):
        for rec in self:
            rec.utilized_qty = 0.00
            # related_sale_order = self.env['sale.order'].search([('project_id', '=', rec.id)])
            related_sale_order =sum(self.env['sale.order'].search([('project_id', '=', self.id)]).mapped('total_utilized'))
            print(related_sale_order)
            if related_sale_order:
                # rec.utilized_qty = related_sale_order.total_utilized
                  rec.utilized_qty = related_sale_order
  

    def _plan_prepare_values(self):
        vals = super(ProjectProjectInherit, self)._plan_prepare_values()
        print(vals)
        vals['dashboard']['profit']['utilized_qty'] = self.utilized_qty
        return vals

