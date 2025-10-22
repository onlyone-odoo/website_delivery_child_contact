import logging
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        """Override cart to add child contacts to qcontext."""
        _logger.info("=== Cart loaded ===")
        response = super(WebsiteSaleCustom, self).cart(access_token, revive, **post)
        order = request.website.sale_get_order(force_create=True)
        if order:
            _logger.info(
                "Order ID: %s, Partner ID: %s",
                order.id,
                order.partner_id.id if order.partner_id else "None",
            )
        else:
            _logger.warning("No order found!")
        child_contacts = request.env["res.partner"]
        if order and order.partner_id:
            all_childs = order.partner_id.child_ids.sudo()
            _logger.info(
                "All child_ids: %s",
                [(c.id, c.name, c.type, c.active) for c in all_childs],
            )
            # Filter to active contacts or delivery types (adjust if only 'contact' is needed)
            child_contacts = all_childs.filtered(
                lambda p: p.type in ("contact", "delivery") and p.active
            )
            _logger.info(
                "Filtered child_contacts: %s",
                [(c.id, c.name, c.type, c.active) for c in child_contacts],
            )
        else:
            _logger.warning("No partner_id in order!")
        response.qcontext["child_contacts"] = child_contacts
        # Add error flag if coming from failed confirmation
        response.qcontext["error"] = post.get("error")
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
        """JSON route to update shipping partner to selected child."""
        _logger.info("=== Select child route hit. child_id from post: %s", child_id)
        data = request.get_json_data()
        child_id = data.get("child_id") if data else child_id
        _logger.info("Parsed child_id: %s (type: %s)", child_id, type(child_id))
        order = request.website.sale_get_order(force_create=True)
        _logger.info("Order ID: %s, Main partner ID: %s", order.id, order.partner_id.id)
        selected = None
        if child_id and child_id != "":
            try:
                child_id_int = int(child_id)
                child = request.env["res.partner"].sudo().browse(child_id_int)
                _logger.info(
                    "Child fetched: ID %s, Name %s, Parent ID %s, Type %s",
                    child.id,
                    child.name,
                    child.parent_id.id if child.parent_id else "None",
                    child.type,
                )
                if (
                    child
                    and child.parent_id.id == order.partner_id.id
                    and child.type in ("contact", "delivery")
                ):
                    order.sudo().write({"partner_shipping_id": child.id})
                    selected = child.name
                    order.env.flush_all()
                    _logger.info(
                        "Updated order %s with shipping_id %s",
                        order.id,
                        order.partner_shipping_id.id,
                    )
                else:
                    _logger.warning(
                        "Validation failed: child %s parent %s != order partner %s, or type %s not in ('contact', 'delivery')",
                        child_id_int,
                        child.parent_id.id if child.parent_id else "None",
                        order.partner_id.id,
                        child.type,
                    )
            except ValueError as e:
                _logger.error("ValueError parsing child_id %s: %s", child_id, e)
        if not selected:
            order.sudo().write({"partner_shipping_id": order.partner_id.id})
            selected = order.partner_id.name
            order.env.flush_all()
            _logger.info(
                "Reset order %s to main partner %s",
                order.id,
                order.partner_shipping_id.id,
            )
        _logger.info("Returning: success=True, selected=%s", selected)
        return {"success": True, "selected": selected}

    @http.route("/shop/confirm_order", type="http", auth="public", website=True)
    def confirm_order(self, **post):
        """Override confirm_order to enforce child selection."""
        order = request.website.sale_get_order()
        if order:
            _logger.info(
                "=== Confirm order hit for order %s. Partner ID: %s, Shipping ID: %s",
                order.id,
                order.partner_id.id,
                order.partner_shipping_id.id if order.partner_shipping_id else "None",
            )
            child_contacts = order.partner_id.child_ids.sudo().filtered(
                lambda p: p.type in ("contact", "delivery") and p.active
            )
            _logger.info(
                "Child contacts in confirm: %s",
                [(c.id, c.name, c.type) for c in child_contacts],
            )
            if child_contacts and order.partner_shipping_id.id == order.partner_id.id:
                _logger.warning(
                    "Confirmation blocked: Shipping ID %s == Partner ID %s, no child selected.",
                    order.partner_shipping_id.id,
                    order.partner_id.id,
                )
                return request.redirect("/shop/cart?error=select_child")
            else:
                _logger.info(
                    "Confirmation allowed: Shipping ID %s is valid child.",
                    order.partner_shipping_id.id,
                )
        return super(WebsiteSaleCustom, self).confirm_order(**post)
