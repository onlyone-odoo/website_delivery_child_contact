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
            _logger.info(
                "Order ID: %s, Partner ID: %s, Partner Name: %s",
                order.id,
                order.partner_id.id,
                order.partner_id.name,
            )
            child_contacts = order.partner_id.child_ids.sudo().filtered(
                lambda p: p.type in ("contact", "delivery") and p.active
            )
            _logger.info(
                "Child Contacts Found: %s",
                [(c.id, c.name, c.type, c.active) for c in child_contacts],
            )
            if not child_contacts:
                _logger.warning(
                    "No child contacts found for partner %s", order.partner_id.id
                )
                # Depurar todos los child_ids sin filtro
                all_childs = order.partner_id.child_ids.sudo()
                _logger.info(
                    "All Child Contacts (no filter): %s",
                    [(c.id, c.name, c.type, c.active) for c in all_childs],
                )
        else:
            _logger.warning(
                "No order or partner found! Order: %s, User: %s",
                order,
                http.request.env.user,
            )
        response.qcontext["child_contacts"] = child_contacts
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
        return http.request.redirect("/shop/cart")
