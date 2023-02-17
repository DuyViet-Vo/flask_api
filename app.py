from flask import Flask,request , jsonify
import json, sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try: 
        conn = sqlite3.connect('books.db')
    except sqlite3.Error as e:
        print(e)
    return conn
        
@app.route('/')
def index():
    return "Helo, vo duy viet"

@app.route('/<name>')
def Show_name(name):
    return "Helo, {}".format(name)

@app.route('/books', methods = ['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor = conn.execute('SELECT * FROM book')
        books = [
            dict(id =row[0],author=row[1],title=row[2])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_title = request.form['title']
        sql = """INSERT INTO book (author, title) VALUES (?,?)"""
        cursor = conn.execute(sql,(new_author,new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully",201
    
@app.route('/books/<int:id>' , methods = ['GET', 'PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute('SELECT * FROM book WHERE id=?', (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book),200
        else:
            return "Something went wrong",404
        
    if request.method == 'PUT':
        sql = """
            UPDATE book SET author = ?, title = ? WHERE id= ?
        """
           
        author = request.form['author']
        title = request.form['title']
                
        update_book = {
            'id': id,
            'author': author,
            'title': title,
        }
        conn.execute(sql,(author,title,id))
        conn.commit()
        return jsonify(update_book)
            
    if request.method == 'DELETE':
        sql = """
            DELETE FROM book WHERE id=?
        """
        conn.execute(sql,(id,))
        conn.commit()
        return 'The book with id: {} has been deleted'.format(id),200
                
    
if __name__ == '__main__':
    app.run(debug=True)