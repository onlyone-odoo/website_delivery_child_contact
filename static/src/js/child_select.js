$(document).ready(function() {
    $('#child_select').on('change', function () {
        var childId = $(this).val();
        console.log('Change event triggered. Selected child_id:', childId);
        if (childId === "") {
            console.log('Placeholder selected, skipping POST.');
            alert("Debe seleccionar un contacto válido.");
            return; // Evita el POST si es el placeholder
        }
        $.ajax({
            url: '/shop/select_child',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ child_id: childId }),
            success: function(response) {
                console.log('AJAX Success:', response);
                if (response.success) {
                    console.log('Selection saved successfully. Selected:', response.selected);
                    location.reload(); // Refresca para actualizar el select
                } else {
                    console.log('Server error:', response.error);
                    alert(response.error);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('AJAX Fail:', textStatus, errorThrown);
                alert('Error: ' + textStatus);
            }
        });
    });
});