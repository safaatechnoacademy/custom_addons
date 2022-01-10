
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import api, fields, models, SUPERUSER_ID, _,exceptions
import logging
_logger = logging.getLogger(__name__)
# from odoo.addons.sale_timesheet.models.project_overview import _plan_prepare_values
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round



class project_sale(models.Model):
    _inherit = 'account.move.line'
    
    utilized_quantity = fields.Float('utilized quantity')


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    utilized_qty = fields.Float(string='Utilized QTY')
    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Launch procurement group run method with required/custom fields genrated by a
        sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
        depending on the sale order line product rule.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        procurements = []
        for line in self:
            if line.state != 'sale' or not line.product_id.type in ('consu','product'):
                continue
            qty = line._get_qty_procurement(previous_product_uom_qty)
            if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
                continue

            group_id = line._get_procurement_group()
            if not group_id:
                group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                line.order_id.procurement_group_id = group_id
            else:
                # In case the procurement group is already created and the order was
                # cancelled, we need to update certain values of the group.
                updated_vals = {}
                if group_id.partner_id != line.order_id.partner_shipping_id:
                    updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
                if group_id.move_type != line.order_id.picking_policy:
                    updated_vals.update({'move_type': line.order_id.picking_policy})
                if updated_vals:
                    group_id.write(updated_vals)

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.product_uom_qty - qty
            my = line.product_uom_qty - self.utilized_qty
            line_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            product_qty, procurement_uom = line_uom._adjust_uom_quantities(my, quant_uom)
            procurements.append(self.env['procurement.group'].Procurement(
                line.product_id, product_qty, procurement_uom,
                line.order_id.partner_shipping_id.property_stock_customer,
                line.name, line.order_id.name, line.order_id.company_id, values))
        if procurements:
            self.env['procurement.group'].run(procurements)
        return True
    
    # def _action_launch_stock_rule(self):
      
    #     for line in self:
    #         my_qty = line.product_uom_qty - self.utilized_qty
    #         product_qty = line.product_uom_qty - self.utilized_qty
    #         quant_uom = line.product_id.uom_id
    #         line_uom = line.product_uom
    #         raise ValidationError(_(line._action_launch_stock_rule(self,product_qty)))
    #     super(SaleOrderLineInherit, self)._action_launch_stock_rule()
    #     order_line = self.env['sale.order.line'].search([('order_id', '=', self.id)])
      

    #     for line in order_line:
    #         self.product_qty = line.product_uom_qty - line.order_id.utilized_qty
        # for line in self:
        #     line.product_qty = line.product_uom_qty - self.utilized_qty
        
        # return res

class SaleOrderInherit(models.Model):

    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project', string='Project')

    total_utilized = fields.Float(compute='_calculate_total_utilized', store=True)

    @api.depends('order_line')
    def _calculate_total_utilized(self):
        for rec in self:
            rec.total_utilized = 0.00
            if rec.order_line:
                rec.total_utilized = sum(rec.order_line.mapped('utilized_qty'))

    def test(self):
        # self.env['stock.move'].search([('product_id', 'in', [product_bolt.id, product_screw.id])])._do_unreserve()
         order_lines = self.env['sale.order.line'].search([('order_id', '=', self.id)])
         raise ValidationError(_(order_lines.utilized_qty))
        #  for pro in order_lines:
        #     move_line = self.env['stock.move'].search([('product_id' , '=' ,pro.product_id.id)])

        
        
        #  order_lines  = self.env['sale.order.line'].search([
        #                 ('order_id', '=', sale_order.id),
        #                 ('product_id', '=', move_line.product_id.id),
                       
        #             ], limit=1)
        #  for product in order_lines:
        #       test = product.qty
        #       product_id = product.product_id
         
         

         
        
         raise ValidationError(_(move_line))

        
        #   raise ValidationError(_(price))


class project_sale(models.Model):
    _inherit = 'account.move.line'

    utilized_quantity = fields.Integer('utilized quantity')


