from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):
    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, **post):
        response = super().cart(**post)
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
    def select_child(self, **post):
        data = http.request.get_json_data()
        child_id = data.get("child_id") if data else None
        order = http.request.website.sale_get_order(force_create=True)
        selected = None
        if child_id and child_id != "":  # Asegurar que no sea el placeholder
            try:
                child_id = int(child_id)
                child = http.request.env["res.partner"].sudo().browse(child_id)
                if (
                    child
                    and child.parent_id.id == order.partner_id.id
                    and child.type in ("contact", "delivery")
                ):
                    order.sudo().write({"partner_shipping_id": child.id})
                    selected = child.name
            except ValueError:
                pass
        if not selected:
            return {"success": False, "error": "Debe seleccionar un contacto válido."}
        return {"success": True, "selected": selected}
