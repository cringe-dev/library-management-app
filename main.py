from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create or initialize SQL db file 'library.db'
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        description TEXT,
        genre TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# Get custom genres fom SQL
def get_genres():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT genre FROM books')
    genres = [row[0] for row in cursor.fetchall()]
    conn.close()
    return genres

# Get list of books for main window
@app.route('/')
def index():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, author FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return render_template('book_detail.html', book=book)

# Sending book info to SQL db
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    all_genres = get_genres()
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        genre = request.form.get('genre')
        custom_genre = request.form.get('custom_genre')
        if genre:
            pass
        else:
            genre = custom_genre

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, description, genre) VALUES (?, ?, ?, ?)',
                       (title, author, description, genre))
        conn.commit()
        conn.close()

    return render_template('add_book.html', genres=all_genres)


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author FROM books WHERE title LIKE ? OR author LIKE ?",
                   ('%' + keyword + '%', '%' + keyword + '%'))
    result = cursor.fetchall()
    conn.close()
    return render_template('search_result.html', result=result)


@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)