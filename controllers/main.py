from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):
    @http.route(
        ["/shop/address"],
        type="http",
        methods=["GET", "POST"],
        auth="public",
        website=True,
        sitemap=False,
    )
    def address(self, **kw):
        response = super(WebsiteSaleCustom, self).address(**kw)
        values = response.qcontext  # Accede a los valores que se pasan a la plantilla

        order = http.request.website.sale_get_order()
        if order and order.partner_id:
            # Obtén todos los contactos hijos del partner actual (usuario activo)
            child_contacts = order.partner_id.child_ids.sudo().filtered(
                lambda p: p.type in ("delivery", "contact") and p.active
            )
            # Reemplaza o une con la lista existente de direcciones (asumiendo key 'addresses')
            values["addresses"] = child_contacts

        return http.request.render("website_sale.address", values)
