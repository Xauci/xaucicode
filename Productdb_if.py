'''
This is the interface to an SQLite Database
'''

import sqlite3

def create_table():
    conn = sqlite3.connect('ProductList.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Productlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            box TEXT,
            dateorder TEXT,
            datepay TEXT,
            payment TEXT,
            price INTEGER,
            status TEXT,
            remarks TEXT)''')
    conn.commit()
    conn.close()

def fetch_productlist():
    conn = sqlite3.connect('ProductList.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ProductList')
    productlist = cursor.fetchall()
    conn.close()
    return productlist

def insert_product(product, box, price, dateorder, datepay, payment, status, remarks):
    conn = sqlite3.connect('ProductList.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ProductList (product, box, price, dateorder, datepay, payment, status, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (product, box, price, dateorder, datepay, payment, status, remarks))
    conn.commit()
    conn.close()

def delete_product(id):
    conn = sqlite3.connect('ProductList.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ProductList WHERE id = ?', (id))
    conn.commit()
    conn.close()

def update_product(new_product, new_box, new_price, new_dateorder, new_datepay, new_payment, new_status, new_remarks, id):
    conn = sqlite3.connect('ProductList.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE ProductList SET product = ?, box = ?, price = ?, dateorder = ?, datepay = ?, payment = ?, status = ?, remarks = ? WHERE id = ?',
                   (new_product, new_box, new_price, new_dateorder, new_datepay, new_payment, new_status, new_remarks, id))
    conn.commit()
    conn.close()


def id_exists(id):
    conn = sqlite3.connect('ProductList.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM ProductList WHERE id = ?', (id))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

create_table()