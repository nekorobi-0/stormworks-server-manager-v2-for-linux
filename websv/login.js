var xhr = new XMLHttpRequest()
xhr.open('POST', `${location.href}`);
xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
xhr.send("rocamisaki is a human");
xhr.onreadystatechange = function(){
    if ((xhr.readyState == 4) && (xhr.status == 200)) {
        let res = xhr.responseText
        if (res != "failed"){
            _return = JSON.parse(res);
            for (let key in _return){
                document.cookie = `${key}=${_return[key]};path=/;`
            };
            window.location.href = `${location.origin}/menu.html`
        }else{
            window.location.href = `${location.origin}/index.html`
        };
    };
};