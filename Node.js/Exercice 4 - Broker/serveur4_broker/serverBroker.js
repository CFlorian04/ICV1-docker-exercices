const http = require('http');
const ip = require('ip');

const requestDelay = 500; // ms

const serverConfig = {
  host: 'localhost', // ip.address()
  port: process.env.PORT,
  response: 'PING',
  name: 'BR'
};

const senderConfig = {
  host: '',
  port: 0,
  name: ''
};

const receiverConfig = {
  host: '',
  port: 0,
  name: ''
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
      console.log(serverConfig.name, ':', receiverConfig.name, ">", content);
    });
  });

  // Gestion des erreurs lors de l'envoi de la requête
  req.on('error', (error) => { raiseError(error) });

  req.end(serverConfig.response);
}

const server = http.createServer((req, res) => {
  let content = '';

  req.on('data', (chunk) => {
    content += chunk;
  });

  getAnnuaire('S1');

  console.log(senderConfig);
  console.log(receiverConfig);

  console.log(serverConfig.name, ':', receiverConfig.name, ">", content);
  
  sendRequest();

});

function getAnnuaire(sender) {
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

        delete serverList[serverConfig.name]

        if (serverList && serverList[sender]) {
          const senderServer = serverList[sender];
          senderConfig.name = senderServer.name;
          senderConfig.host = senderServer.host;
          senderConfig.port = senderServer.port;

          console.log(senderConfig);

          delete serverList[sender];

          if (Object.keys(serverList)[0]) {
            const receiverServer = serverList[Object.keys(serverList)[0]];
            receiverConfig.name = receiverServer.name;
            receiverConfig.host = receiverServer.host;
            receiverConfig.port = receiverServer.port;

            console.log(receiverConfig);

          } else {
            console.log("Le serveur cible n'a pas été trouvé dans la liste.");
          }

        } else {
          console.log("Le serveur expéditeur n'a pas été trouvé dans la liste.");
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

});
