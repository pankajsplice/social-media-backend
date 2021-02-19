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

$("#logout").click(function (e) {
    e.preventDefault();
    let auth="Token "+localStorage.getItem('key');
    let csrftoken = readCookie('csrftoken');
        $.ajax({
            url: document.location.origin + '/api/accounts/logout/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': auth,
                "X-CSRFToken": csrftoken,
            },
            credentials: 'same-origin',
            success: function (response) {
                localStorage.removeItem('key');
                localStorage.setItem('user', false);
//                alert("Successfully Logged out");
                document.location.href=document.location.origin + '/login/';
            },
            error: function (response, jqXhr) {
               let error = JSON.parse(response.responseText);
               alert(error.detail);

            }

        })

});

//user logout header

$("#profile_logout").click(function (e) {
    e.preventDefault();
    let auth="Token "+localStorage.getItem('key');
    let csrftoken = readCookie('csrftoken');
        $.ajax({
            url: document.location.origin + '/api/accounts/logout/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': auth,
                "X-CSRFToken": csrftoken,
            },
            credentials: 'same-origin',
            success: function (response) {
                localStorage.removeItem('key');
                localStorage.setItem('user', false);
//                alert("Successfully Logged out");
                document.location.href=document.location.origin + '/login/';
            },
            error: function (response, jqXhr) {
               let error = JSON.parse(response.responseText);
               alert(error.detail);

            }

        })

});