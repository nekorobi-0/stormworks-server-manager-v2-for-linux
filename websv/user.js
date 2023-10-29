function login() {
    var getCookie = (function(){
        return function() {
         var result = [];
         var cookies = document.cookie;
       
         if(cookies != ''){
          var cookieArray = cookies.split(';');
          for(var i = 0; i < cookieArray.length; i++){
           var cookie = cookieArray[i].split('=');
           result[cookie[0]] = decodeURIComponent(cookie[1]);
          }
         }
         return result;
        };
       })();
    if (id in getCookie){
        var fd = new FormData();
        fd.append('id',getCookie['id']);
        fd.append('seckey',getCookie['seckey']);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', `https://${location.origin}/api/login_with_cookie`);
        xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        xhr.send(fd);
        xhr.onreadystatechange = function(){
            if ((xhr.readyState == 4) && (xhr.status == 200)) {
                _return = JSON.parse(xhr.responseText);
                for (let key in _return){
                    document.cookie = key +'=' + _return[key];
                };
            };
        };
    } else{
        xhr.open('POST', `https://${location.origin}/api/login_with_misskey`);
        xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        xhr.send('stormskey');
        xhr.onreadystatechange = function(){
            if ((xhr.readyState == 4) && (xhr.status == 200)) {
                _return = JSON.parse(xhr.responseText);
                for (let key in _return){
                    document.cookie = key +'=' + _return[key];
                };
            };
        };
    };
};
function logon() {//サーバーにみすきーの認証をリクエスト
    var xhr = new XMLHttpRequest();
    logout()
    xhr.open('POST', `https://${location.origin}/api/logon_url`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr.send( 'rocamisaki is very hentai' );
    xhr.onreadystatechange = function(){
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            _return = JSON.parse(xhr.responseText);
            url = _return["url"];
            var div = document.getElementById("MisskeyAuth");
            div.innerHTML = `<button type="button" class="btn btn-outline-success btn-lg" onclink ="window.open='${url}'">押してください</button>`
        };
    };
};
function logout(){
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i]
        const eqPos = cookie.indexOf('=')
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie
        document.cookie = name + '=;max-age=0'
    };
};