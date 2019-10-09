var sqlite = require('sqlite-sync');
 
//Connecting
sqlite.connect('database.db');


function save(){
    var login = document.getElementById('email').value;
    var senha = document.getElementById('senha').value;
    db.transaction(function(armazenar){
        armazenar.executeSql('INSERT INTO usuario (email,senha) VALUES (?,?)',[login,senha]);
    });
}
