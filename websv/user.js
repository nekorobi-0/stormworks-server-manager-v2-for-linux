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
    if (id in getCookie){//クッキーに情報がある場合
        window.location.href('menu.html')//ユーザーページにリダイレクト
    } else{//クッキーに情報がない場合の処理
        let misskeyurl = document.getElementById('misskeyurl');
        xhr.open('POST', `https://${location.origin}/api/login_with_misskey`);
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
            url = xhr.responseText;
            open(url);
        };
    };
};
function logout(){//クッキー全削除
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i]
        const eqPos = cookie.indexOf('=')
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie
        document.cookie = name + '=;max-age=0'
    };
};