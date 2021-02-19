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

                $('#profile_icon_name2').text(data.first_name +' '+data.last_name);
                $('#profile_phone').text(data.profile.mobile);
                $('#profile_email').text(data.email);
                $('#profile_last_name').text(data.last_name);
                $('#profile_first_name').text(data.first_name );
                $("#profile_icon4").attr("src", data.profile.profile_pic);
             }
        }).catch((error) => {
            if(error){
            console.log(error)
//                document.location.href=document.location.origin +'/login/';
            }
        });
    }

