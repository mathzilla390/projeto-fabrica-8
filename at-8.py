from flask import Flask, jsonify, request, Response
app = Flask(__name__)
playlist = [
    {"id": 1, "titulo": "Astronomia", "artista": "Tony Igy", "duracao": 236, "url": "..."}]
proximo_id = 2
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API está no ar!"}), 200
@app.route("/tracks", methods=["GET", "POST"])
def tracks_collection():
    global proximo_id
    if request.method == "GET":
        return jsonify(playlist), 200
    dados = request.get_json()
    campos_obrigatorios = ["titulo", "artista", "duracao"]
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos 'titulo', 'artista' e 'duracao' são obrigatórios."}), 400
    nova_musica = {"id": proximo_id,
        "titulo": dados["titulo"],
        "artista": dados["artista"],
        "duracao": dados["duracao"],
        "url": dados.get("url", "")}
    playlist.append(nova_musica)
    proximo_id += 1
    return jsonify(nova_musica), 201
@app.route("/tracks/<int:track_id>", methods=["GET", "PUT", "DELETE"])
def track_resource(track_id):
    musica = next((t for t in playlist if t["id"] == track_id), None)
    if musica is None:
        return jsonify({"erro": f"Música com ID {track_id} não encontrada."}), 404
    if request.method == "GET":
        return jsonify(musica), 200
    elif request.method == "PUT":
        dados = request.get_json()
        for campo in ["titulo", "artista", "duracao", "url"]:
            if campo in dados:
                musica[campo] = dados[campo]
        return jsonify(musica), 200
    elif request.method == "DELETE":
        playlist.remove(musica)
        return Response(status=204)
if __name__ == "__main__":
    app.run(debug=True)
