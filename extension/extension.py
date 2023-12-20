from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello_world():
    args = request.args
    prompt = args.get("prompt")
    data = {
      "output": "hello"
    }
    if prompt == "French":
        data["output"] = "bonjour"
    elif prompt == "Spanish":
        data["output"] = "hola"

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))