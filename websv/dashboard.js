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
            let htmltxt = ""
            for (let key in _return){
                htmltxt += `<tr>
                <th scope="row">${key}</th>
                <td>${_return[key]}</td>
                <td>
                    <button type="button" class="btn btn-success" onclick=reqest("run",${key})>Run</button>
                    <button type="button" class="btn btn-primary" onclick=reqest("edit",${key})>Edit</button>
                    <button type="button" class="btn btn-danger" onclick=reqest("delete",${key})>Delete</button>
                </td>
                </tr>`
            };
            document.getElementById('table2').innerHTML = htmltxt
            //window.location.href = `${location.origin}/menu.html`
        }else{
            //window.location.href = `${location.origin}/index.html`
        };
    };
};
function reqest(mode,id){
    var xhr = new XMLHttpRequest()
    xhr.open('POST', `${location.origin}/api/oparates`);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    var cookie = getCookie();
    var obj = {
        "id":cookie["id"],
        "seacret":cookie["seacret"],
        "mode":mode,
        "id":id
    }
    xhr.send(JSON.stringify(obj));
    xhr.onreadystatechange = function(){
    };
};