import socket, json, sys

def run_server():
    HOST = '127.0.0.1'
    PORT = 8080

    server_list = { "s1": { "host": HOST, "port": 4567 }, "s2": { "host": HOST, "port": 5372 }, "br": { "host": HOST, "port": 1111 }}
    annuaireSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        annuaireSocket.bind((HOST, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()

    while True:
        print("Serveur prêt, en attente de requêtes ...")
        annuaireSocket.listen(2)
        connexion, adresse = annuaireSocket.accept()
        print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

        connexion.send(json.dumps(server_list).encode("utf-8"))

if __name__ == "__main__":
    run_server()