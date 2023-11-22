import errno, socket, sys, time, json, os

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
    print("Server Pong run")
    HOST = '0.0.0.0'
    PORT = 5372

    receiver_code = "s1"
    receiver_HOST = ''
    receiver_PORT = 0

    annuaire_HOST = os.environ.get("MEDIATOR_URL", HOST)
    annuaire_PORT = 8080

    # Création du socket :
    serveurSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Nombre maximal de tentatives de connexion
    max_attempts = 5
    current_attempt = 0

    print("Annuaire : ", annuaire_HOST)

    # Récupération des informations de l'annuaire
    while current_attempt < max_attempts:
        try:
            annuaireSocket.connect((annuaire_HOST, annuaire_PORT))
            messageReceive = json.loads(annuaireSocket.recv(1024).decode("Utf8"))
            receiver_HOST = messageReceive[receiver_code]["host"]
            receiver_PORT = int(messageReceive[receiver_code]["port"])
            print("Annuaire, adresse IP %s, port %s" % (receiver_HOST, receiver_PORT))
            break  # Si la connexion réussit, sortir de la boucle
        except socket.error as e:
            current_attempt += 1
            print(f"La tentative de connexion a échoué (tentative {current_attempt}/{max_attempts}). Erreur: {e}")
            time.sleep(1)  # Attendre 1 seconde avant la prochaine tentative
            #if current_attempt == max_attempts:
                #sys.exit()
        finally:
            annuaireSocket.close()  # Fermer la connexion après la tentative, qu'elle réussisse ou échoue

    # Connexion au serveur Ping
    try:
        receiverSocket.connect((receiver_HOST, receiver_PORT))
    except socket.error as e:
        print(f"La connexion a échoué. Erreur {e}")
        if e.errno == errno.ECONNREFUSED:
            print(f"Le serveur Pong n'est peut-être pas encore prêt. Réessayer dans quelques secondes.")
        else:
            print(os.strerror(socket.error))
        #sys.exit()

    # Ouverture du serveur
    try:
        serveurSocket.bind((HOST, PORT))
    except socket.error as e:
        print(f"La liaison du socket à l'adresse choisie a échoué. Erreur {e}")
        #sys.exit()
        
    while True:
        print("Serveur prêt, en attente de requêtes ...")
        serveurSocket.listen()
        connexion, adresse = serveurSocket.accept()
        print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))
        
        get_message(receiverSocket, receiver_code, "PONG", connexion)

if __name__ == "__main__":
    run_server()