var getCookie = (function(){
    return function() {
     var result = [];
     var cookies = document.cookie;
   
     if(cookies != ''){
      var cookieArray = cookies.split(';');
      for(var i = 0; i < cookieArray.length; i++){
       var cookie = cookieArray[i].split('=');
       cookie[0] = cookie[0].replace('"',"").replace(" ","")
       let l = cookie.length
       let cont = cookie[1]
       for (let i=2;i < l;i++){
           cont = cont + "=" + cookie[i]
       }
       result[cookie[0]] = decodeURIComponent(cont);
      }
     }
     return result;
    };
})();
function get_profile(){
    var xhr = new XMLHttpRequest()
    xhr.open('POST', `${location.origin}/api/get_profile`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    var cookie = getCookie();
    var obj = {
        "id":cookie["id"],
        "seacret":cookie["seacret"],
        "mode":"addadmin",
        "proid":cookie["editor"]
    }
    xhr.send(JSON.stringify(obj));
    xhr.onreadystatechange = function(){
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            let res = xhr.responseText
            if (res != "failed"){
                _return = JSON.parse(res);
                for (let key in _return){
                    let doc = document.getElementById(key);
                    doc.value =  _return[key];
                };
            }else{
                window.location.href = `${location.origin}/index.html`
            };
        };
    };
};
function addadmin(){
    let add_id = document.getElementById('Adminid');
    var xhr = new XMLHttpRequest()
    xhr.open('POST', `${location.origin}/api/oparation`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    var cookie = getCookie();
    var obj = {
        "id":cookie["id"],
        "seacret":cookie["seacret"],
        "mode":"addadmin",
        "proid":cookie["editor"],
        "add_id":add_id
    }
    xhr.send(JSON.stringify(obj));
};
function save(){
    let add_id = document.getElementById('Adminid');
    var xhr = new XMLHttpRequest()
    xhr.open('POST', `${location.origin}/api/oparation`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    var cookie = getCookie();
    form = document.forms['myform']
    var obj = {
        "id":cookie["id"],
        "seacret":cookie["seacret"],
        "mode":"addadmin",
        "proid":cookie["editor"],
        "add_id":add_id
    }
    xhr.send(JSON.stringify(obj));
};
get_profile()