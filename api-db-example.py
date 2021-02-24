import flask
import psycopg2
from flask import request, jsonify, make_response
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World!</h1><p>From Python and Flask!</p>"


@app.route('/api/books/add', methods=['POST'])
def api_add():
    # print(request.form)
    title = request.form['title']
    author = request.form['author']
    try:
        connection = psycopg2.connect(user="krisszafranski",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="php_books")
        # Avoid getting arrays of arrays!
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        print(title, author)
        insertQuery = "INSERT INTO books (title, author) VALUES (%s, %s)"
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, (title, author))
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "Book inserted")
        # respond nicely
        result = {'status': 'CREATED'}
        return make_response(jsonify(result), 201)
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        if(connection):
            print("Failed to insert book", error)
            # respond with error
            result = {'status': 'ERROR'}
            return make_response(jsonify(result), 500)
    finally:
        # closing database connection.
        if(connection):
            # clean up our connections
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/api/books/all', methods=['GET'])
def api_all():
    connection = psycopg2.connect(user="krisszafranski",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="php_books")

    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM books"
    # execute query
    cursor.execute(postgreSQL_select_Query)
    # Selecting rows from mobile table using cursor.fetchall
    books = cursor.fetchall()
    # respond, status 200 is added for us
    return jsonify(books)

    # for row in books:
    #     print("Id = ", row[0], )
    #     print("Title = ", row[1])
    #     print("Author  = ", row[2], "\n")


app.run()