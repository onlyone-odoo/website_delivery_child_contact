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
            child_contacts = all_childs.filtered(
                lambda p: p.type in ("contact", "delivery") and p.active
            )
            _logger.info(
                "Child contacts for order %s: %s",
                order.id,
                child_contacts.mapped("name"),
            )
        response.qcontext["child_contacts"] = child_contacts
        return response

    @http.route(
        ["/shop/select_child"],
        type="json",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def select_child(self, child_id=None, **post):
        _logger.info(f"Received POST with child_id: {post.get('child_id')}")
        order = http.request.website.sale_get_order(force_create=True)
        _logger.info(
            "Select child called for order %s with child_id: %s", order.id, child_id
        )
        selected = None
        if child_id:
            try:
                child_id = int(child_id)
                child = http.request.env["res.partner"].sudo().browse(child_id)
                _logger.info(
                    "Child found: %s, parent: %s, type: %s",
                    child.name,
                    child.parent_id.id,
                    child.type,
                )
                if (
                    child
                    and child.parent_id.id
                    == order.partner_id.id  # Compara IDs explícitamente
                    and child.type in ("contact", "delivery")
                ):
                    order.sudo().write({"partner_shipping_id": child.id})
                    selected = child.name
                    _logger.info(
                        "Write successful, new shipping_id: %s",
                        order.partner_shipping_id.id,
                    )
                else:
                    _logger.warning("Condition failed for child %s", child_id)
            except ValueError as e:
                _logger.error("Invalid child_id: %s, error: %s", child_id, str(e))
        if not selected:
            order.sudo().write({"partner_shipping_id": order.partner_id.id})
            selected = order.partner_id.name
            _logger.info(
                "Reset to parent, shipping_id: %s", order.partner_shipping_id.id
            )
        return {"success": True, "selected": selected}
