# Définition d'un serveur réseau/
# Attente de la connexion d'un client
import socket, sys, time, json
HOST = '127.0.0.1'
PORT = 5372

s1_HOST = ''
s1_PORT = ''

annuaire_HOST = HOST
annuaire_PORT = 8080

# Création du socket :
serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Récupération des informations de l'annuaire
try:
    annuaireSocket.connect((annuaire_HOST, annuaire_PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()

while 1:
    msgClient = annuaireSocket.recv(1024).decode("Utf8")
    msgClient = json.loads(msgClient)
    s1_HOST = msgClient["s1"]["host"]
    s1_PORT = msgClient["s1"]["port"]
    print("Annuaire, adresse IP %s, port %s" % (s1_HOST, s1_PORT))
    break


# Liaison du socket à une adresse précise :
try:
    clientSocket.connect((s1_HOST, s1_PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()

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
    
    # Dialogue avec le client :
    msgClient = connexion.recv(1024).decode("Utf8")
    while 1:
        if msgClient.upper() == "END":
            break
        print("S1>", msgClient)
        msgServeur = "PONG"
        clientSocket.send(msgServeur.encode("Utf8"))
        time.sleep(0.5)
        msgClient = connexion.recv(1024).decode("Utf8")
        print("S2>", msgServeur)
        
    # Fermeture de la connexion :
    print("Connexion interrompue.")
    connexion.close()
    break