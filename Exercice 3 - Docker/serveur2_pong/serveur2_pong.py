import socket, sys, time, json, os

# Envoi d'un message
def send_message(socket, receiver_code, message, connexion):
    messageSend = { "receiver" : receiver_code, "message" : message }
    socket.send(json.dumps(messageSend).encode("Utf8"))
    print("S2>", messageSend["message"])
    time.sleep(0.5)
    get_message(socket, receiver_code, message, connexion)

# Reception d'un message
def get_message(socket, receiver_code, message, connexion):
    messageReceive = connexion.recv(1024).decode("Utf8")
    messageReceive = json.loads(messageReceive)
    print("S1>", messageReceive["message"])
    time.sleep(0.5)
    send_message(socket, receiver_code, message, connexion)

def run_server():
    HOST = '0.0.0.0'
    PORT = 5372

    receiver_code = "s1"
    receiver_HOST = ''
    receiver_PORT = 0

    annuaire_HOST = os.environ.get("MEDIATOR_URL", "http://ex3_annuaire:8080")
    annuaire_PORT = 8080

    # Création du socket :
    serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Récupération des informations de l'annuaire
    try:
        annuaireSocket.connect((annuaire_HOST, annuaire_PORT))
        messageReceive = json.loads(annuaireSocket.recv(1024).decode("Utf8"))
        receiver_HOST = messageReceive[receiver_code]["host"]
        receiver_PORT = int(messageReceive[receiver_code]["port"])
        print("Annuaire, adresse IP %s, port %s" % (receiver_HOST, receiver_PORT))
    except socket.error:
        print("La connexion a échoué.") 
        sys.exit()

    # Connexion au broker
    try:
        receiverSocket.connect((receiver_HOST, receiver_PORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()

    # Ouverture du serveur
    try:
        serveurSocket.bind((HOST, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()
        
    while True:
        print("Serveur prêt, en attente de requêtes ...")
        serveurSocket.listen(2)
        connexion, adresse = serveurSocket.accept()
        print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))
        
        get_message(receiverSocket, receiver_code, "PONG", connexion)

if __name__ == "__main__":
    run_server()