const http = require('http');
const ip = require('ip');

const requestDelay = 500; // ms

const serverConfig = {
  host: 'localhost', // ip.address()
  port: process.env.PORT,
  response: 'PONG',
  name: 'S2'
};

const receiverConfig = {
  host: '',
  port: 0,
  name: 'BR'
};

const annuaireConfig = {
  host: 'serveurannuaire',//process.env.MEDIATOR_URL || 'annuaire-container',
  port: 8080
};

function raiseError(error) {
  console.error(serverConfig.name, "> Erreur d'envoi de requête :", error.message);
  //process.exit(1);
}

// Envoyer une requête HTTP
function sendRequest() {
  const options = {
    hostname: receiverConfig.host,
    port: receiverConfig.port,
    path: '/',
    method: 'GET'
  };

  const req = http.request(options, (res) => {
    let content = '';

    res.on('data', (chunk) => {
      content += chunk;
    });

    res.on('end', () => {
      console.log(receiverConfig.name, ">", content);
    });
  });

  // Gestion des erreurs lors de l'envoi de la requête
  req.on('error', (error) => { raiseError(error) });

  req.write(serverConfig.name+'>'+serverConfig.response)

  req.end(serverConfig.response);
}

const server = http.createServer((req, res) => {
  console.log(serverConfig.name, ">", serverConfig.response);
  res.end(serverConfig.response);

  setTimeout(() => {
    sendRequest();
  }, requestDelay);
});

function getAnnuaire() {
  const options = {
    hostname: annuaireConfig.host,
    port: annuaireConfig.port,
    path: '/',
    method: 'GET'
  };

  const req = http.request(options, (res) => {
    let content = '';

    res.on('data', (chunk) => {
      content += chunk;
    });

    res.on('end', () => {
      try {
        const serverList = JSON.parse(content);

        if (serverList && serverList[receiverConfig.name]) {

          const targetServer = serverList[receiverConfig.name];
          receiverConfig.host = targetServer.host;
          receiverConfig.port = targetServer.port;

          sendRequest();

        } else {
          console.log("Le serveur cible n'a pas été trouvé dans la liste.");
        }
      } catch (error) {
        raiseError(error);
      }
    });
  });

  req.on('error', (error) => {
    raiseError(error);
  });

  req.end();
}

// Gestion des erreurs lors du démarrage du serveur
server.on('error', (error) => { raiseError(error) });

server.listen(serverConfig.port, () => {

  console.log(serverConfig.name, "> Listening on PORT", serverConfig.port);
  console.log(serverConfig.name, "> Open on http://" + serverConfig.host + ":" + serverConfig.port);
  getAnnuaire();

});
