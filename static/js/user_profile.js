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
            return response.json();
        }).then(data => {
               localStorage.setItem("user",data.username);

        }).catch((error) => {
            console.error('Error:', error);
        });
    }
if(localStorage.getItem("user")){
       let user = localStorage.getItem("user");
       let menu = '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"> Welcome,'+
        ' '+user+
        '<span class="caret"></span></a>'+
        '<ul class="dropdown-menu">'+
            '<li><a href="/changepassword">Change Password</a></li>'+
            '<li><a id="logout" href="">Logout</a></li>'+
        '</ul>';
        $('#item').append(menu);
   }
else{
        let menu = '<li><a href="/login">Login Here</a></li>'+
                    '<li><a href="/register">Register Here</a></li>';
                    $('#item').append(menu);
    }