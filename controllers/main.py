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
        order = http.request.website.sale_get_order(force_create=True)
        selected = None
        if child_id:
            child = http.request.env["res.partner"].sudo().browse(int(child_id))
            if (
                child
                and child.parent_id == order.partner_id
                and child.type in ("contact", "delivery")
            ):
                order.sudo().partner_shipping_id = (
                    child  # Usa sudo() para write seguro en portal
                )
                selected = child.name
        else:
            order.sudo().partner_shipping_id = order.partner_id
            selected = order.partner_id.name
        order.env.flush_all()  # Forza flush a DB para persistir cambios inmediatamente
        _logger.info(
            "Updated order %s with shipping_id %s",
            order.id,
            order.partner_shipping_id.id,
        )
        return {"success": True, "selected": selected}
