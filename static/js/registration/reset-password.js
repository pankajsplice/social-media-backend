function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
$("#send_mail").click(function (e) {
    e.preventDefault();
    let email = document.getElementById('id_email').value;
    let csrftoken = readCookie('csrftoken');
    if(email ===''){
        $('#id_email_errors').html('<li> Email can not be blank </li>');
    }
    else{
        $.ajax({
            url: document.location.origin + '/api/accounts/password/reset/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken,
            },
            credentials: 'same-origin',
            dataType: "json",
            data: JSON.stringify({
                email: email,
            }),
            success: function (response) {
                console.log(response);
                localStorage.setItem('user', false);
                localStorage.removeItem('key');
                document.location.href=document.location.origin+'/password-reset-done/';
            },
            error: function (data, jqXhr) {
            $.each(data.responseJSON, function (fieldName, errorBag) {

					var errorsDivId = "#id_" + fieldName + "_errors";
					var htmlToInsert = "";
					if(fieldName=='detail' || fieldName=='non_field_errors'){
					    htmlToInsert += '<li>* ' + errorBag + '</li>';
					}
					else{
					    $.each(errorBag, function(i, error) {
						    htmlToInsert += '<li>* ' + error + '</li>';
					    });
					}
					// output each error message for this field
					$(errorsDivId).html(htmlToInsert);
				});
            }

        })

    }

});