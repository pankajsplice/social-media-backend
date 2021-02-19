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
$("#user_login").click(function (e) {
    e.preventDefault();
    let email = document.getElementById('id_username').value;
    let password = document.getElementById('id_password').value;
    let csrftoken = readCookie('csrftoken');
    if(email ===''){
        $('#id_email_errors').html('<li> Email can not be blank </li>');
    }
    else if(password===''){
         $('#id_password_errors').html('<li>Password can not be blank</li>');
    }
    else{
        $.ajax({
            url: document.location.origin + '/api/accounts/login/',
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
                username: email,
                password: password,
            }),
            success: function (response) {
                console.log(response);
                if (response.status === 200) {
                    localStorage.setItem('email', email);
                }
                let key = response.key;
                localStorage.setItem('user',true);
                localStorage.setItem('key',key);
//                alert("Successfully Logged in");
                document.location.href=document.location.origin +'/profile/';
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