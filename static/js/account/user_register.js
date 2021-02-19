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
$('#user_registration').click(function (e) {
   e.preventDefault();
   let first_name = document.getElementById('id_first_name').value;
   let last_name = document.getElementById('id_last_name').value;
   let phone = document.getElementById('id_mobile').value;
   let email = document.getElementById('id_email').value;
   let pass1 = document.getElementById('id_password1').value;
   let type = document.getElementById('id_type').value;
   let profile_pic = $('#id_profile_pic')[0].files[0];
   let csrftoken = readCookie('csrftoken');
    var formData = new FormData();
    formData.append("username", email);
    formData.append("email", email);
    formData.append("password1", pass1);
    formData.append("password2", pass1);
    formData.append("first_name", first_name);
    formData.append("last_name", last_name);
    formData.append("mobile", phone);
    formData.append("type", type);
    if(profile_pic)formData.append("profile_pic", profile_pic);
    else formData.append("profile_pic", null);
     if (first_name==='')
       alert("First Name can't be blank");
   else if(last_name==='')
       alert("Last Name can't be blank");
   else if(phone==='')
       alert("Phone no. can't be blank");
   else if( email==='')
       alert("Email can't be blank");
   else if(pass1==='')
       alert("Password can't be blank");
   else {
            fetch(document.location.origin+'/api/registrations/', {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body:formData
        }).then(response => {
             if (!response.ok) throw response;
                return response.json();

        }).then(data => {
            console.log(data);
            if(data.key){
                        localStorage.setItem('key',data.key);
                        localStorage.setItem('user', true);
                        document.location.href=document.location.origin + '/profile/';
            }
            else{
                alert(data.detail);
            }

        }).catch((error) => {
            error.json().then((body) => {
                $.each(body, function (fieldName, errorBag) {
                    console.log(fieldName, errorBag);
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
            });
        });
   }
});
