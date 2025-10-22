odoo.define('website_delivery_child_contact.child_select', ['web.public.widget', 'web.core'], function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;  // For translations

    publicWidget.registry.WebsiteSaleChildSelect = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'change #child_select': '_onChangeChildSelect',
        },

        start: function () {
            this._super.apply(this, arguments);
            this._toggleCheckoutButton();
        },

        _onChangeChildSelect: function (ev) {
            var $select = $(ev.currentTarget);
            var child_id = $select.val();
            console.log('Change event triggered. Selected child_id:', child_id);

            if (child_id === "") {
                console.log('Placeholder selected, skipping POST.');
                alert(_t("Debe seleccionar un contacto válido."));  // Translatable alert, matching your original
                this._toggleCheckoutButton();
                return;
            }

            var self = this;
            $.jsonRpc('/shop/select_child', 'call', {child_id: child_id}).then(function (result) {
                if (result.success) {
                    console.log('Selected:', result.selected);
                    // Optional: Update UI without reload, e.g., show a confirmation message
                    self._showSuccessMessage(result.selected);
                }
            }).fail(function (error, event) {
                console.log('JSON-RPC Fail:', error);
                alert(_t('Error al seleccionar: ') + (error.message || _t('Error desconocido.')));
            });

            this._toggleCheckoutButton();
        },

        _toggleCheckoutButton: function () {
            var $select = $('#child_select');
            var $checkoutBtn = $('a[href="/shop/checkout"]');
            if ($select.length && $select.val() === '') {
                $checkoutBtn.addClass('disabled').attr('title', _t('Please select a child contact first.'));
            } else {
                $checkoutBtn.removeClass('disabled').removeAttr('title');
            }
        },

        _showSuccessMessage: function (selectedName) {
            // Optional: Add a temporary success message near the select
            var $message = $('<div class="alert alert-success mt-2">').text(_t('Seleccionado: ') + selectedName);
            $('#child_select').after($message);
            setTimeout(function () {
                $message.fadeOut('slow', function () { $(this).remove(); });
            }, 3000);
        },
    });

    return publicWidget.registry.WebsiteSaleChildSelect;
});