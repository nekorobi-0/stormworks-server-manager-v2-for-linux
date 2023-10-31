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
let data = getCookie()
document.getElementById('icon').innerHTML = (`
    <img src="${data["avatarurl"]}" alt="" width="32" height="32" class="rounded-circle me-2">
    <strong>${data["username"]}</strong>`);
if (data["id"] == undefined){
    window.location.href = `${location.origin}/index.html`
}