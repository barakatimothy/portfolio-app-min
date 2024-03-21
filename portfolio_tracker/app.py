# app.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 symbol TEXT NOT NULL,
                 purchase_price REAL NOT NULL,
                 quantity INTEGER NOT NULL,
                 date_acquired DATE NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Route to display the portfolio
@app.route('/')
def portfolio():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("SELECT * FROM assets")
    assets = c.fetchall()
    conn.close()
    return render_template('portfolio.html', assets=assets)

# Route to add an asset to the portfolio
@app.route('/add_asset', methods=['POST'])
def add_asset():
    symbol = request.form['symbol']
    purchase_price = request.form['purchase_price']
    quantity = request.form['quantity']
    date_acquired = request.form['date_acquired']
    
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("INSERT INTO assets (symbol, purchase_price, quantity, date_acquired) VALUES (?, ?, ?, ?)",
              (symbol, purchase_price, quantity, date_acquired))
    conn.commit()
    conn.close()
    
    return redirect(url_for('portfolio'))

if __name__ == '__main__':
    app.run(debug=True)
