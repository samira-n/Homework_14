from flask import Flask, jsonify
from utils import search_by_title

app = Flask(__name__)


@app.route("/movie/<title>")
def title_page(title):
    search_title = search_by_title(title)
    return jsonify(search_title)


app.run(debug=True)


if __name__ == "__main__":
    app.run()
