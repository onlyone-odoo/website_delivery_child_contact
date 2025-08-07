from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):
    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        response = super(WebsiteSaleCustom, self).cart(access_token, revive, **post)
        order = http.request.website.sale_get_order()
        if order and order.partner_id:
            child_contacts = order.partner_id.child_ids.sudo().filtered(
                lambda p: p.type in ("contact", "delivery") and p.active
            )
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
            if (
                child
                and child.parent_id == order.partner_id
                and child.type in ("contact", "delivery")
            ):
                order.partner_shipping_id = child
        else:
            order.partner_shipping_id = order.partner_id  # Reset a "yo mismo"
        return http.request.redirect("/shop/cart")
