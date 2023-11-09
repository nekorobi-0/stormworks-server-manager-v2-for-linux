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
function get_admin(){
    var xhr = new XMLHttpRequest()
    xhr.open('POST', `${location.origin}/api/get_admin`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    var cookie = getCookie();
    var obj = {
        "id":cookie["id"],
        "seacret":cookie["seacret"],
        "proid":cookie["editor"]
    }
    xhr.send(JSON.stringify(obj));
    xhr.onreadystatechange = function(){
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            let res = xhr.responseText
            if (res != "failed"){
                _return = JSON.parse(res);
                let doc = document.getElementById("table");
                let htmltxt = ""
                for (let key in _return){
                    htmltxt += `
                        <tr>
                            <th scope="row">${key}</th>
                            <td>
                                <button type="button" class="btn btn-danger onclick=deladmin(${key})">Delete</button>
                            </td>
                        </tr>`
                };
                doc.innerHTML = htmltxt
            }else{
                window.location.href = `${location.origin}/index.html`
            };
        };
    };
};
function deladmin(id){
    console.log(mode)
    var xhr = new XMLHttpRequest()
    xhr.open('POST', `${location.origin}/api/oparation`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    var cookie = getCookie();
    var obj = {
        "id":cookie["id"],
        "seacret":cookie["seacret"],
        "mode":"deladmin",
        "proid":cookie["editor"],
        "id2del":id
    }
    xhr.send(JSON.stringify(obj));
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
        "proid":Number(cookie["editor"]),
        "add_id":add_id.value
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
        "mode":"save",
        "proid":cookie["editor"],
        "add_id":add_id,
        "datas":{
            "name":getdata("name"),
            "password":getdata("password"),
            "base_island":getdata("base_island"),
            "seed":getdata("seed"),
            "max_players":getdata("max_players"),
            "dlc_arid":getdata("dlc_arid"),
            "dlc_weapons":getdata("dlc_weapons"),
            "dlc_space":getdata("dlc_space")
        }
    };
    xhr.send(JSON.stringify(obj));
};
function getdata(id){
    let add_id = document.getElementById(id).value;
    return add_id;
};
get_profile()