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
var xhr = new XMLHttpRequest()
xhr.open('POST', `${location.origin}/api/get_profiles`);
xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
var cookie = getCookie();
var obj = {
    "id":cookie["id"],
    "seacret":cookie["seacret"]
}
xhr.send(JSON.stringify(obj));
xhr.onreadystatechange = function(){
    if ((xhr.readyState == 4) && (xhr.status == 200)) {
        let res = xhr.responseText
        if (res != "failed"){
            _return = JSON.parse(res);
            for (let key in _return){
                
            };
            window.location.href = `${location.origin}/menu.html`
        }else{
            //window.location.href = `${location.origin}/index.html`
        };
    };
};