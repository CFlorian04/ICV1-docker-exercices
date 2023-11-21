import socket, sys, time, json
HOST = '127.0.0.1'
PORT = 4567

serveurPongHOST = HOST
serveurPongPORT = 5372

# Création des sockets :
serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveurPong = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        serveurPong.connect((serveurPongHOST, serveurPongPORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    
    send_message(serveurPong, "PING", connexion)
        
    # Fermeture de la connexion :
    print("Connexion interrompue.")
    connexion.close()
    break