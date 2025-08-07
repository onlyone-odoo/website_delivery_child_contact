from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        response = super(WebsiteSaleCustom, self).cart(access_token, revive, **post)
        order = http.request.website.sale_get_order()
        child_contacts = http.request.env["res.partner"]
        if order and order.partner_id:
            _logger.info("Order Partner ID: %s", order.partner_id.id)
            child_contacts = order.partner_id.child_ids.sudo().filtered(
                lambda p: p.type in ("contact", "delivery") and p.active
            )
            _logger.info("Child Contacts: %s", child_contacts)
            response.qcontext["child_contacts"] = child_contacts
        else:
            _logger.warning("No order or partner found in cart!")
        _logger.info("QContext keys: %s", response.qcontext.keys())
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
            if (
                child
                and child.parent_id == order.partner_id
                and child.type in ("contact", "delivery")
            ):
                order.partner_shipping_id = child
                _logger.info("Selected shipping partner: %s", child.name)
        else:
            order.partner_shipping_id = order.partner_id
            _logger.info("Reset to main partner: %s", order.partner_id.name)
        return http.request.redirect("/shop/cart")
