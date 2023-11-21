import socket, sys, time, json
HOST = '127.0.0.1'
PORT = 4567

brokerHOST = ''
brokerPORT = ''

annuaire_HOST = HOST
annuaire_PORT = 8080

# Création des sockets :
serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
brokerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

messageSend = { "receiver" : "s2", "message" : '' }
messageReceive = ''

# Envoi d'un message
def send_message(socket, message, connexion):
    messageSend["message"] = message
    socket.send(json.dumps(messageSend).encode("Utf8"))
    print("S1>", messageSend["message"])
    time.sleep(0.5)
    get_message(socket, message, connexion)

# Reception d'un message
def get_message(socket, message, connexion):
    messageReceive = connexion.recv(1024).decode("Utf8")
    messageReceive = json.loads(messageReceive)
    print("S1>", messageReceive["message"])
    time.sleep(0.5)
    send_message(socket, message, connexion)

# Récupération des informations de l'annuaire
try:
    annuaireSocket.connect((annuaire_HOST, annuaire_PORT))
    annuaireArray = annuaireSocket.recv(1024).decode("Utf8")
    annuaireArray = json.loads(annuaireArray)
    brokerHOST = annuaireArray["s2"]["host"]
    brokerPORT = annuaireArray["s2"]["port"]
    print("Annuaire, adresse IP %s, port %s" % (brokerHOST, brokerPORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()

# Ouverture du serveur
try:
    serveurSocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit
    
while 1:
    # Attente de la requête de connexion d'un client :
    print("Serveur prêt, en attente de requêtes ...")
    serveurSocket.listen(2)
    # Etablissement de la connexion :
    connexion, adresse = serveurSocket.accept()
    print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

    try:
        brokerSocket.connect((brokerHOST, brokerPORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    
    send_message(brokerSocket, "PING", connexion)
        
    # Fermeture de la connexion :
    print("Connexion interrompue.")
    connexion.close()
    break