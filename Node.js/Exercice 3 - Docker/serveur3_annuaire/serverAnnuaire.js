const http = require('http');
const ip = require('ip');

const serverConfig = {
  host: 'localhost', // ip.address()
  port: process.env.PORT,
  name: 'AN'
};

const serverList = {
  "S1": { host: 'serveurping', port: 4567 },
  "S2": { host: 'serveurpong', port: 5372 }
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
  console.log(serverConfig.name, "> Open on http://" + serverConfig.host + ":" + serverConfig.port);
});

