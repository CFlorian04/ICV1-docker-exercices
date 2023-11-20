# Définition d'un serveur réseau/
# Attente de la connexion d'un client
import socket, sys, time
HOST = '127.0.0.1'
PORT = 4567

count_limit = 10
count_msg_send = 0

s2_HOST = HOST
s2_PORT = 5372

# Création du socket :
serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        clientSocket.connect((s2_HOST, s2_PORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    
    # Dialogue avec le client :
    msgServeur = "PING"
    clientSocket.send(msgServeur.encode("Utf8"))
    count_msg_send = count_msg_send + 1
    print("S1>", msgServeur)
    time.sleep(0.5)
    msgClient = connexion.recv(1024).decode("Utf8")
    while 1:
        print("S2>", msgClient)
        if count_msg_send == count_limit:
            msgServeur = "END"
            clientSocket.send(msgServeur.encode("Utf8"))
            break
        msgServeur = "PING"
        clientSocket.send(msgServeur.encode("Utf8"))
        count_msg_send = count_msg_send + 1
        time.sleep(0.5)
        msgClient = connexion.recv(1024).decode("Utf8")
        print("S1>", msgServeur)
        
    # Fermeture de la connexion :
    print("Connexion interrompue.")
    connexion.close()
    break