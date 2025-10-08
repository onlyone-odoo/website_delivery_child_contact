$(document).ready(function() {
    $('#child_select').on('change', function() {
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
                console.log('AJAX Success - Full response:', response);
                var result = response.result || response;  // Desenvuelve el JSON-RPC envelope
                console.log('Unwrapped result:', result);  // Log para confirmar {success: true, selected: 'hijo 1'}
                if (result.success) {
                    console.log('Selection saved successfully. Selected:', result.selected);
                    location.reload();  // Refresca para actualizar el select
                } else {
                    var errorMsg = result.error || 'Error desconocido del servidor (sin mensaje).';
                    console.log('Server error:', errorMsg);
                    alert(errorMsg);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('AJAX Fail:', textStatus, errorThrown);
                alert('Error: ' + textStatus);
            }
        });
    });
});