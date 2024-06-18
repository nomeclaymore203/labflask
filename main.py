from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("dbname=db1 user=postgres password=457389d437d437a370 host=127.0.0.1 port=5432")
cursor = conn.cursor()

createtable = """CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);"""
cursor.execute(createtable)
conn.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor.execute("DELETE FROM notes WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (title, content, id))
        conn.commit()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM notes WHERE id = %s", (id,))
        note = cursor.fetchone()
        return render_template('edit.html', note=note)

if __name__ == '__main__':
    app.run(debug=True)
