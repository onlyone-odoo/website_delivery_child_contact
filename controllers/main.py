from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        _logger.info("=== Custom Cart Controller Called ===")
        response = super(WebsiteSaleCustom, self).cart(access_token, revive, **post)
        order = http.request.website.sale_get_order(force_create=True)
        child_contacts = http.request.env["res.partner"]
        _logger.info(
            "User: %s (ID: %s)", http.request.env.user.name, http.request.env.user.id
        )
        if order and order.partner_id:
            _logger.info("Order ID: %s, Partner ID: %s", order.id, order.partner_id.id)
            all_childs = order.partner_id.child_ids.sudo()
            _logger.info(
                "All Childs: %s", [(c.id, c.name, c.type, c.active) for c in all_childs]
            )
            child_contacts = all_childs.filtered(lambda p: p.active)
            _logger.info(
                "Filtered Childs: %s",
                [(c.id, c.name, c.type, c.active) for c in child_contacts],
            )
        else:
            _logger.info("No order or partner!")
        response.qcontext["child_contacts"] = child_contacts
        _logger.info("QContext keys: %s", response.qcontext.keys())
        return response

    # Mantén el select_child igual

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
        return http.request.redirect("/shop/cart")
