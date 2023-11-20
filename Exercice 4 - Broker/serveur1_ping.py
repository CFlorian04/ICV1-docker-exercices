# Définition d'un serveur réseau/
# Attente de la connexion d'un client
import socket, sys, time, json
HOST = '127.0.0.1'
PORT = 4567

count_limit = 10
count_msg_send = 0

brokerHOST = ''
brokerPORT = ''

annuaire_HOST = HOST
annuaire_PORT = 8080

# Création du socket :
serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
brokerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

messageSend = { "receiver" : "s2", "message" : '' }
messageReceive = ''

def send_message(socket, message, count_msg_send):
    messageSend["message"] = message
    socket.send(json.dumps(messageSend).encode("Utf8"))
    count_msg_send = count_msg_send + 1
    print("S1>", messageSend["message"])

def get_message(connexion):
    messageReceive = connexion.recv(1024).decode("Utf8")
    messageReceive = json.loads(messageReceive)
    print("S1>", messageReceive["message"])

# Récupération des informations de l'annuaire
try:
    annuaireSocket.connect((annuaire_HOST, annuaire_PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()

while 1:
    annuaireArray = annuaireSocket.recv(1024).decode("Utf8")
    annuaireArray = json.loads(annuaireArray)
    brokerHOST = annuaireArray["br"]["host"]
    brokerPORT = annuaireArray["br"]["port"]
    print("Annuaire, adresse IP %s, port %s" % (brokerHOST, brokerPORT))
    break

# Liaison du socket à une adresse précise :
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
    
    # Dialogue avec le client :
    send_message(brokerSocket, "PING", count_msg_send)
    time.sleep(0.5)
    get_message(connexion)

    while 1:
        if count_msg_send == count_limit:
            send_message(brokerSocket, "END", count_msg_send)
            break

        send_message(brokerSocket, "PING", count_msg_send)
        time.sleep(0.5)
        get_message(connexion)
        
    # Fermeture de la connexion :
    print("Connexion interrompue.")
    connexion.close()
    break