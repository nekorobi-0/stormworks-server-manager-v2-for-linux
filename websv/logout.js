function logout(){//クッキー全削除
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i]
        const eqPos = cookie.indexOf('=')
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie
        document.cookie = name + '=;max-age=0'
    };
    window.location.href = `${location.origin}/index.html`;
};