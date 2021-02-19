if(localStorage.getItem('key')!==null){
    let url=document.location.origin+"/api/accounts/user/";
    let auth="Token "+localStorage.getItem('key');
    fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': auth,
            },
        }).then(response => {
             if (!response.ok) throw response;
                return response.json();
        }).then(data => {
        console.log("data", data)
            if(data.pk !== 1){
                document.getElementById("id_mobile").value = data.profile.mobile;
                document.getElementById("id_email").value = data.email;
                document.getElementById("id_last_name").value = data.last_name;
                document.getElementById("id_first_name").value = data.first_name;
                $("#profile_icon4").attr("src", data.profile.profile_pic);
                $('#id_type').val(data.profile.type);
             }
        }).catch((error) => {
            if(error){
            console.log(error)
//                document.location.href=document.location.origin +'/login/';
            }
        });
    }

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
$('#update_profile').click(function (e) {
   e.preventDefault();
   let first_name = document.getElementById('id_first_name').value;
   let last_name = document.getElementById('id_last_name').value;
   let username =  document.getElementById("id_email").value;
   let phone = document.getElementById('id_mobile').value;
   let profile_pic = $('#id_profile_pic')[0].files[0];
   let csrftoken = readCookie('csrftoken');
    var formData = new FormData();
    formData.append("first_name", first_name);
    formData.append("username", username);
    formData.append("last_name", last_name);
//    var profile_details = JSON.stringify({"mobile": phone});
    formData.append("profile.mobile", phone);
//    formData.append("profile", {"mobile": phone});

    if(profile_pic)formData.append("profile.profile_pic", profile_pic);
    console.log(formData);
            fetch(document.location.origin+'/api/accounts/user/', {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body:formData
        }).then(response => {
             if (!response.ok) throw response;
                return response.json();

        }).then(data => {
            console.log(data);
//            alert('profile updated successfully')
            localStorage.setItem('user', true);
            document.location.href=document.location.origin + '/update-profile/';

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
});