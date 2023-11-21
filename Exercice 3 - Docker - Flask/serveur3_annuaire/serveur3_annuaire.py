from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def annuaire():
    HOST = '0.0.0.0'
    PORT = 8080

    server_list = {"s1": {"host": HOST, "port": 4567}, "s2": {"host": HOST, "port": 5372}, "br": {"host": HOST, "port": 1111}}

    # Placeholder response for testing purposes
    return jsonify(server_list)

if __name__ == "__main__":
    print("Run Server Annuaire")
    app.run(host='0.0.0.0', port=8080)
