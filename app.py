from flask import Flask, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)

# Datenbankverbindung herstellen
conn = sqlite3.connect('urls.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS urls (short TEXT, full TEXT)')
conn.commit()

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>URL Shortener</h1>
    <form action="/shorten" method="post">
        <input type="text" name="url" placeholder="Geben Sie die zu kürzende URL ein" required>
        <input type="submit" value="Kürzen">
    </form>
    '''

@app.route('/shorten', methods=['POST'])
def shorten():
    full_url = request.form['url']
    short_code = generate_short_code()
    c.execute('INSERT INTO urls (short, full) VALUES (?, ?)', (short_code, full_url))
    conn.commit()
    return f'''
    <p>Ihre gekürzte URL: <a href="/{short_code}">http://localhost:5000/{short_code}</a></p>
    '''

@app.route('/<short_code>')
def redirect_short_url(short_code):
    c.execute('SELECT full FROM urls WHERE short=?', (short_code,))
    result = c.fetchone()
    if result:
        return redirect(result[0])
    else:
        return 'URL nicht gefunden', 404

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)


