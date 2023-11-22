import socket, sys, time, json
HOST = '127.0.0.1'
PORT = 5372

brokerHOST = ''
brokerPORT = ''

annuaire_HOST = HOST
annuaire_PORT = 8080

# Création du socket :
serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveurPing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

messageSend = { "receiver" : "s1", "message" : '' }
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
    messageReceive = json.loads(annuaireSocket.recv(1024).decode("Utf8"))
    brokerHOST = messageReceive["s1"]["host"]
    brokerPORT = messageReceive["s1"]["port"]
    print("Annuaire, adresse IP %s, port %s" % (brokerHOST, brokerPORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()

# Connexion au broker
try:
    serveurPing.connect((brokerHOST, brokerPORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()

# Ouverture du serveur
try:
    serveurSocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
    
while 1:
    print("Serveur prêt, en attente de requêtes ...")
    serveurSocket.listen(2)
    connexion, adresse = serveurSocket.accept()
    print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))
    
    get_message(serveurPing, "PONG", connexion)
        
    # Fermeture de la connexion :
    print("Connexion interrompue.")
    connexion.close()
    break