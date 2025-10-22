(function () {
    'use strict';

    $(document).ready(function() {
        toggleCheckoutButton();  // Check initial state

        $('#child_select').on('change', function() {
            var childId = $(this).val();
            console.log('Change event triggered. Selected child_id:', childId);
            if (childId === "") {
                console.log('Placeholder selected, skipping POST.');
                alert("Debe seleccionar un contacto válido.");
                toggleCheckoutButton();
                return;
            }
            $.ajax({
                url: '/shop/select_child',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ child_id: childId }),
                success: function(response) {
                    console.log('AJAX Success - Full response:', response);  // Log completo para depurar
                    if (response.success) {
                        console.log('Selection saved successfully. Selected:', response.selected);
                        showSuccessMessage(response.selected);
                    } else {
                        var errorMsg = response.error || 'Error desconocido del servidor.';
                        console.log('Server error:', errorMsg);
                        alert(errorMsg);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('AJAX Fail:', textStatus, errorThrown);
                    alert('Error: ' + textStatus);
                }
            });
            toggleCheckoutButton();
        });
    });

    function toggleCheckoutButton() {
        var $select = $('#child_select');
        var $checkoutBtn = $('a[href="/shop/checkout"]');
        if ($select.length && $select.val() === '') {
            $checkoutBtn.addClass('disabled').attr('title', 'Please select a child contact first.');
        } else {
            $checkoutBtn.removeClass('disabled').removeAttr('title');
        }
    }

    function showSuccessMessage(selectedName) {
        // Optional: Temporary success message without reload
        var $message = $('<div class="alert alert-success mt-2">').text('Seleccionado: ' + selectedName);
        $('#child_select').after($message);
        setTimeout(function () {
            $message.fadeOut('slow', function () { $(this).remove(); });
        }, 3000);
    }
})();