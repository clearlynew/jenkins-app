from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="root",
        database="librarydb"
    )

@app.route("/init", methods=["GET"])
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            author VARCHAR(100),
            price INT,
            status VARCHAR(20),
            borrowed_by VARCHAR(100)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    return "Database initialized"

@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, price, status, borrowed_by) VALUES (%s, %s, %s, %s, %s)",
        (data["title"], data["author"], data["price"], "Available", None)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Book added"})

@app.route("/books", methods=["GET"])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["PUT"])
def borrow_book(book_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET status=%s, borrowed_by=%s WHERE id=%s",
        ("Borrowed", data["borrowed_by"], book_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Book borrowed"})

@app.route("/books/<int:book_id>", methods=["DELETE"])
def sell_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Book sold"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

