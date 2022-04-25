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


    @app.route('/movie/<int:year_start>/to/<int:year_end>')
    def get_movie_year(year_start, year_end):
        query = f"""
            SELECT title,release_year
            FROM netflix
            WHERE release_year BETWEEN '{year_start}' AND '{year_end}'
            ORDER BY release_year DESC
            LIMIT 100
        """
        response = get_db(query)
        response_json = []
        for movie in response:
            response_json.append({
                'title': movie[0],
                'release_year': movie[1]
            })
        return jsonify(response_json)


    @app.route('/rating/<group>')
    def get_movie_rating(group):
        levels = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'adult': ['R', 'NC-17']
        }
        if group in levels:
            level = '\", \"'.join(levels[group])
            level = f'\"{level}\"'
        else:
            return jsonify([])

        query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({level})
        """

        response = get_db(query)
        response_json = []
        for movie in response:
            response_json.append({
                'title': movie[0],
                'rating': movie[1],
                'description': movie[2],
            })
        return jsonify(response_json)

    @app.route('/genre/<genre>')
    def get_genre(genre):
        query = f"""
                SELECT title
                FROM netflix
                WHERE listed_in LIKE '%{genre}%'
                ORDER BY release_year DESC
                LIMIT 10
            """
        response = get_db(query)
        response_json = []
        for genre in response:
            response_json.append({
                'title': genre[0]
            })
        return jsonify(response_json)


    def get_cast(name1='Rose McIver', name2='Ben Lamb'):
        query = f"""
            SELECT `cast`
            FROM netflix 
            WHERE `cast` LIKE '%{name1}%' 
            AND `cast` LIKE '%{name2}%'
        """
        response = get_db(query)
        actors = []
        for cast in response:
            actors.extend(cast[0].split(', '))
        result = []
        for a in actors:
            if a not in [name1, name2]:
                if actors.count(a) > 2:
                    result.append(a)
        result = set(result)
        print(result)

    #get_cast()


    #app.run(debug=True)


if __name__ == "__main__":
    main()
