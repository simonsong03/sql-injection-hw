from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("names.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS names")
        cursor.execute('''CREATE TABLE IF NOT EXISTS names (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL)''')
        cursor.execute("INSERT OR IGNORE INTO names (id, name) VALUES (1, 'Simon'), (2, 'Yvonne'), (3, 'Matthew'), (4, 'Chris'), (5, 'Caleb')")
        conn.commit()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Name Search</title>
    </head>
    <body>
        <h1>Search for a Name</h1>
        <form method="post" action="/search">
            <input type="text" name="name" placeholder="Enter a name" required>
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    '''

@app.route('/search', methods=['POST'])
def search_name():
    name = request.form.get("name")
    with sqlite3.connect("names.db") as conn:
        cursor = conn.cursor()

        ### This is where the query is parameterized and protected
        cursor.execute("SELECT * FROM names WHERE name = ?", (name,))
        ### ---------------------------------------------------------\
        
        result = cursor.fetchall()
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Name Search</title>
    </head>
    <body>
        <h1>Search for a Name</h1>
        <form method="post" action="/search">
            <input type="text" name="name" placeholder="Enter a name" required>
            <button type="submit">Search</button>
        </form>
        <h2>Result:</h2>
        {f'<p>Name found: {result}</p>' if result else '<p>No match found.</p>'}
    </body>
    </html>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
