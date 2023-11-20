import socket, json, sys

HOST = '127.0.0.1'
PORT = 8080

s1_HOST = HOST
s1_PORT = 4567

s2_HOST = HOST
s2_PORT = 5372

data = {
    "s1": { "host":HOST, "port":4567 }, 
    "s2": { "host":HOST, "port":5372 },
    "br": { "host":HOST, "port":1111 },
}

# Création du socket :
annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison du socket à une adresse précise :
try:
    annuaireSocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()

while True:
    # Attente de la requête de connexion d'un client :
    print("Serveur prêt, en attente de requêtes ...")
    annuaireSocket.listen(2)
    # Etablissement de la connexion :
    connexion, adresse = annuaireSocket.accept()
    print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))


    # Convertir le dictionnaire en une chaîne JSON
    msgServeur = json.dumps(data)

    # Envoyer la chaîne JSON encodée en UTF-8
    connexion.send(msgServeur.encode("utf-8"))
    #print("A>", msgServeur)

    # Fermeture de la connexion :
    print("Connexion interrompue.")
    connexion.close()
