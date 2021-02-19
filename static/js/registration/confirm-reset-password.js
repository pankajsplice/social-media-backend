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
$("#update_password").click(function (e) {
    e.preventDefault();
    let password1 = document.getElementById('id_new_password1').value;
    let password2 = document.getElementById('id_new_password2').value;
    let csrftoken = readCookie('csrftoken');
    if(password1 ===''){
        $('#id_new_password1_errors').html('<li> Password1 can not be blank </li>');
    }
    else if(password2===''){
         $('#id_new_password2_errors').html('<li> Confirm Password can not be blank</li>');
    }
    else{
        $.ajax({
            url: document.location.origin + '/api/accounts/password/change/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken,
            },
            credentials: 'same-origin',
            dataType: "json",
            data: JSON.stringify({
                new_password1: password1,
                new_password2: password2
            }),
            success: function (response) {
                console.log(response);
                localStorage.setItem('user', false);
                localStorage.removeItem('key');
                alert("Password Changed Successfully ");
                document.location.href=document.location.origin+'/password-reset-complete/';
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