$(document).ready(function() {
    $('#child_select').on('change', function () {
        var childId = $(this).val();
        console.log('Changing to child_id:', childId);
        if (childId === "") {
            alert("Debe seleccionar un contacto válido.");
            return; // Evita el POST si es el placeholder
        }
        $.ajax({
            url: '/shop/select_child',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ child_id: childId }),
            success: function(response) {
                if (response.success) {
                    console.log('Success:', response);
                    location.reload();
                } else {
                    alert(response.error);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Fail:', textStatus, errorThrown);
                alert('Error: ' + textStatus);
            }
        });
    });
});