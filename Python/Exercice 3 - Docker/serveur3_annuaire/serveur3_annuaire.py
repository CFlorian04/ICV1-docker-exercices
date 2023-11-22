import socket, json, sys

def run_server():
    print("Server Annuaire run")

    HOST = '0.0.0.0'
    PORT = 8080

    server_list = { 
        "s1": { "host": HOST, "port": 4567 }, 
        "s2": { "host": HOST, "port": 5372 }
    }

    annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        annuaireSocket.bind((HOST, PORT))
    except socket.error as e:
        print(f"La liaison du socket à l'adresse choisie a échoué. Erreur {e}")
        sys.exit()

    print("Serveur prêt, en attente de requêtes ...")
    annuaireSocket.listen()

    while True:
        connexion, adresse = annuaireSocket.accept()
        print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

        try:
            connexion.send(json.dumps(server_list).encode("utf-8"))
        finally:
            connexion.close()  # Fermer la connexion après l'envoi de la réponse

if __name__ == "__main__":
    run_server()