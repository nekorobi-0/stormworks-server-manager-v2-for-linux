
var getCookie = (function(){
    return function() {
    var result = [];
    var cookies = document.cookie;
    if(cookies != ''){
        var cookieArray = cookies.split(';');
        for(var i = 0; i < cookieArray.length; i++){
            var cookie = cookieArray[i].split('=');
            result[cookie[0]] = decodeURIComponent(cookie[1]);
        };
    };
    return result;
    };
})();
if (" id" in getCookie()){//クッキーに情報がある場合
    window.location.href = 'menu.html';//ユーザーページにリダイレクト
};
function login() {
    //クッキーに情報がない場合の処理
    var xhr = new XMLHttpRequest();
    let input = document.getElementById('misskeyurl');
    let misskeyurl = input.value;
    console.log(misskeyurl);
    xhr.open('POST', `${location.origin}/api/login_with_misskey`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr.send(misskeyurl);
    document.getElementById('show').innerHTML = 'みすきーに認証urlを送信しました'
};
function logon() {//サーバーにみすきーの認証をリクエスト
    var xhr = new XMLHttpRequest();
    logout()
    xhr.open('POST', `${location.origin}/api/logon_url`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr.send( 'rocamisaki is very hentai' );
    xhr.onreadystatechange = function(){
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            url = xhr.responseText;
            document.getElementById('show').innerHTML = `<a href="${url}"><p>click me</p></a>`;
        };
    };
};