from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

html = '''
<!doctype html>
<title>Specimen Size Calculator</title>
<h2>Enter Specimen Data</h2>
<form method=post>
  Username: <input type=text name=username><br>
  Microscope Size (mm): <input type=number step=0.01 name=microscope_size><br>
  Magnification: <input type=number step=0.01 name=magnification><br>
  <input type=submit value=Submit>
</form>
{% if result %}
  <h3>Real Size: {{ result }} mm</h3>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        username = request.form['username']
        microscope_size = float(request.form['microscope_size'])
        magnification = float(request.form['magnification'])
        real_size = microscope_size / magnification
        conn = sqlite3.connect("specimen_data.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS specimens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                microscope_size REAL,
                magnification REAL,
                real_size REAL
            )
        ''')
        cursor.execute('''
            INSERT INTO specimens (username, microscope_size, magnification, real_size)
            VALUES (?, ?, ?, ?)
        ''', (username, microscope_size, magnification, real_size))
        conn.commit()
        conn.close()
        result = real_size
    return render_template_string(html, result=result)

if __name__ == '__main__':
    app.run(debug=True)