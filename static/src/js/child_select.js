$(document).ready(function() {
    $('#child_select').on('change', function () {
        var childId = $(this).val();
        console.log('Change event triggered. Selected child_id:', childId);
        if (childId === "") {
            console.log('Placeholder selected, skipping POST.');
            alert("Debe seleccionar un contacto válido.");
            return;
        }
        $.ajax({
            url: '/shop/select_child',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ child_id: childId }),
            success: function(response) {
                console.log('AJAX Success - Full response:', response);  // Log full para ver qué llega
                if (response.success) {
                    console.log('Selection saved successfully. Selected:', response.selected);
                    location.reload();  // Refresca para actualizar el select
                } else {
                    var errorMsg = response.error || 'Error desconocido del servidor (sin mensaje).';
                    console.log('Server error:', errorMsg);
                    alert(errorMsg);
                    // Opcional: no reload si error, o sí para resetear
                    // location.reload();
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('AJAX Fail - Status:', textStatus, 'Error:', errorThrown, 'Response:', jqXHR.responseText);
                alert('Error AJAX: ' + textStatus + ' - ' + (errorThrown || 'Sin detalles'));
            }
        });
    });
});