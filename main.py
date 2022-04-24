from flask import Flask, jsonify
import sqlite3


def main():

    app = Flask(__name__)

    def get_db(query):
        with sqlite3.connect("netflix.db") as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    @app.route('/movie/<title>')
    def get_title(title):
        query = f"""
            SELECT title, country, release_year, listed_in AS genre, description, type
            FROM netflix
            WHERE title = '{title}'
            AND type = 'Movie'
            ORDER BY release_year DESC
            LIMIT 1
        """
        response = get_db(query)[0]
        response_json = {
            'title': response[0],
            'country': response[1],
            'release_year': response[2],
            'genre': response[3],
            'description': response[4],
            'type': response[5]
        }
        return jsonify(response_json)



    app.run(debug=True)


if __name__ == "__main__":
    main()
