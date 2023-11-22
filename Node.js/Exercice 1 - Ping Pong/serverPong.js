const http = require('http');

const requestDelay = 500; // ms

const serverConfig = {
  port: 5372,
  response: 'PONG',
  name: 'S2'
};

const receiverConfig = {
  host: 'localhost',
  port: 4567,
  name: 'S1'
};


function raiseError(error) {
  console.error(serverConfig.name, "> Erreur d'envoi de requête :", error.message);
  process.exit(1);
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

  req.end(serverConfig.response);
}

const server = http.createServer((req, res) => {
  console.log(serverConfig.name, ">", serverConfig.response);
  res.end(serverConfig.response);

  setTimeout(() => {
    sendRequest();
  }, requestDelay);
});

// Gestion des erreurs lors du démarrage du serveur
server.on('error', (error) => { raiseError(error) });

server.listen(serverConfig.port, () => {

  console.log(serverConfig.name, "> Listening on PORT", serverConfig.port);
  //sendRequest();

});