xhr.open('POST', `${location.origin}/api/login_with_misskey`);
xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
xhr.send(misskeyurl);
xhr.onreadystatechange = function(){
    if ((xhr.readyState == 4) && (xhr.status == 200)) {
        _return = JSON.parse(xhr.responseText);
        for (let key in _return){
            document.cookie = key +'=' + _return[key];
        };
    };
};