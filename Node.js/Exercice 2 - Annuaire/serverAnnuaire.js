// annuaireServer.js
const http = require('http');

const serverConfig = {
  port: 8080,
  name: 'AN'
};

const serverList = {
    "S1": {host: 'localhost', port: 4567},
    "S2": {host: 'localhost', port: 5372}
}

const server = http.createServer((req, res) => {

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(serverList));

    console.log(serverConfig.name, "> New request");

});

// Gestion des erreurs lors du démarrage du serveur annuaire
server.on('error', (error) => {
  console.error(serverConfig.name, ">", "Erreur lors du démarrage du serveur annuaire :", error.message);
  process.exit(1);
});

server.listen(serverConfig.port, () => {
  console.log(serverConfig.name, "> Listening on PORT", serverConfig.port);
});

