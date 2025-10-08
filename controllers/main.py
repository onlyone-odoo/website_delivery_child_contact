from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        _logger.info("=== Cart loaded ===")
        response = super(WebsiteSaleCustom, self).cart(access_token, revive, **post)
        order = http.request.website.sale_get_order(force_create=True)
        if order:
            _logger.info(
                "Order ID: %s, Partner ID: %s",
                order.id,
                order.partner_id.id if order.partner_id else "None",
            )
        else:
            _logger.warning("No order found!")
        child_contacts = http.request.env["res.partner"]
        if order and order.partner_id:
            all_childs = order.partner_id.child_ids.sudo()
            _logger.info(
                "All child_ids: %s",
                [(c.id, c.name, c.type, c.active) for c in all_childs],
            )
            # Temporal: sin filtro de tipo para depurar; restaura después
            child_contacts = all_childs.filtered(lambda p: p.active)
            _logger.info(
                "Filtered child_contacts: %s",
                [(c.id, c.name, c.type, c.active) for c in child_contacts],
            )
        else:
            _logger.warning("No partner_id in order!")
        response.qcontext["child_contacts"] = child_contacts
        _logger.info("qcontext keys: %s", response.qcontext.keys())
        return response

    @http.route(
        ["/shop/select_child"],
        type="json",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def select_child(self, child_id=None, **post):
        child_id = post.get("child_id")  # Más seguro para POST
        order = http.request.website.sale_get_order(force_create=True)
        selected = None
        if child_id and child_id != "":
            try:
                child_id = int(child_id)
                child = http.request.env["res.partner"].sudo().browse(child_id)
                if (
                    child
                    and child.parent_id == order.partner_id
                    and child.type in ("contact", "delivery")
                ):
                    order.sudo().write({"partner_shipping_id": child.id})
                    selected = child.name
                    order.env.flush_all()  # Forza persistencia
                    _logger.info(
                        "Updated order %s with shipping_id %s",
                        order.id,
                        order.partner_shipping_id.id,
                    )
            except ValueError:
                pass
        if not selected:
            order.sudo().write({"partner_shipping_id": order.partner_id.id})
            selected = order.partner_id.name
            order.env.flush_all()
            _logger.info(
                "Reset order %s to main partner %s",
                order.id,
                order.partner_shipping_id.id,
            )
        return {"success": True, "selected": selected}
