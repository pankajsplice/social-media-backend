$("#user_login").click(function (e) {
    e.preventDefault();
    let email = document.getElementById('id_username').value;
    let password = document.getElementById('id_password').value;
    if(email ==='' || password===''){
        alert('Fields can not be blank');
    }
    else{
        $.ajax({
            url: document.location.origin + '/api/accounts/login/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
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
                localStorage.setItem('user',email);
                localStorage.setItem('key',key);
                let url=document.location.origin+"/api/accounts/user/";
                let auth="Token "+localStorage.getItem('key');
                $.ajax({
                    url: url,
                    type: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': auth,
                    },

                   success: function (response) {
                            localStorage.setItem("userName",response.username);
                            localStorage.setItem("firstName",response.first_name);
                            localStorage.setItem("lastName",response.last_name);
                            localStorage.setItem("userPK",response.pk);
                   }


                })
                alert("Successfully Logged in");
                document.location.href=document.location.origin;
            },
            error: function (response, jqXhr) {
               let error = JSON.parse(response.responseText);
               if (error.email)
                   alert(error.email);
               if (error.non_field_errors)
                   alert(error.non_field_errors);

            }

        })

    }

});