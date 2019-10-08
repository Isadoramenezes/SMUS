var db = openDatabase("BancoTeste", "2.0", "database", 4048);
db.transaction(function(criar){
    criar.executeSql("CREATE TABLE users (ID PRIMARY KEY, nome TEXT, senha TEXT)");
});
function save(){
    var user = document.getElementById('user').value;
    var senha = document.getElementById('senha').value;
    db.transaction(function(armazenar){
        armazenar.executeSql('INSERT INTO users (user,senha) VALUES (?,?)',[user,senha]);
    });
}