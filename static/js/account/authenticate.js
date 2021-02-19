if(localStorage.getItem('user')=='false'){
    document.location.href=document.location.origin +'/login/';
}
else{
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

                $('#profile_icon_name1').text(data.first_name +' '+data.last_name);
                $('#profile_icon_email').text(data.email);
                $("#profile_icon1").attr("src", data.profile.profile_pic);
                $("#profile_icon2").attr("src", data.profile.profile_pic);
                $("#profile_icon3").attr("src", data.profile.profile_pic);

             }
        }).catch((error) => {
            if(error){
            console.log(error)
//                document.location.href=document.location.origin +'/login/';
            }
        });
    }
}