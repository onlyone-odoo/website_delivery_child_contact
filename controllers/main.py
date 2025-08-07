from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        response = super(WebsiteSaleCustom, self).cart(access_token, revive, **post)
        order = http.request.website.sale_get_order(force_create=True)
        child_contacts = http.request.env["res.partner"]
        if order and order.partner_id:
            all_childs = order.partner_id.child_ids.sudo()
            child_contacts = all_childs.filtered(lambda p: p.active)
        response.qcontext["child_contacts"] = child_contacts
        return response

    @http.route(
        ["/shop/select_child"],
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def select_child(self, child_id=None, **post):
        order = http.request.website.sale_get_order(force_create=True)
        if child_id:
            child = http.request.env["res.partner"].sudo().browse(int(child_id))
            if child and child.parent_id == order.partner_id:
                order.partner_shipping_id = child
                _logger.info(
                    "Selected shipping partner: %s (ID: %s)", child.name, child.id
                )
        else:
            order.partner_shipping_id = order.partner_id
            _logger.info(
                "Reset to main partner: %s (ID: %s)",
                order.partner_id.name,
                order.partner_id.id,
            )
        # En lugar de redirect, seguimos al siguiente paso (checkout)
        return http.request.redirect("/shop/checkout")
