$(document).ready(function() {
    $('#child_select').on('change', function () {
        var childId = $(this).val();
        console.log('Changing to child_id:', childId);
        $.post('/shop/select_child', { child_id: childId }).done(function (response) {
            console.log('Success:', response);
            location.reload(); // Refresca para ver el cambio
        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.error('Fail:', textStatus, errorThrown);
            alert('Error: ' + textStatus);
        });
    });
});