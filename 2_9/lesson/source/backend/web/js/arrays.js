

function is_auth(login,pass){
    for(let user of users){
        if(user.login == login && user.password == pass) {
            return true;
        }
    }
    return false;
}


users = [{
    'login':'admin',
    'password':'123'
    },
    {
        'login':'test',
        'password':'123'
    }
]

users.push({'login':'demo','password':'321'});
//
// alert(users.indexOf({'login':'admin','password':'123'}));

