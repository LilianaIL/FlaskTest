from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os
from werkzeug.utils import secure_filename
import sqlite3
from io import BytesIO

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

app = Flask(__name__)

#formtarget="_blank"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_to_database(filename,file.read())
    return redirect('/')

@app.route('/')
def index():
    files=get_all_documents()
    return render_template('home.html', files=files)

@app.route('/aboute')
def about_index():
    return render_template('about.html')

@app.route('/documents')
def documents():
    files=get_all_documents()
    return send_file(files[0].data,attachment_filename=files[0].name)

#FUNCTIONS

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def get_all_documents():
    conn=sqlite3.connect("Files.db")
    conn.row_factory=sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM FilesTbl""")
    files = []
    data = cursor.fetchall()
    for row_data in data:
        files.append(file_init(row_data))
    conn.commit()
    cursor.close()
    conn.close()
    return files

def upload_to_database(file_name, file_data):
    conn = sqlite3.connect("Files.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS FilesTbl (file_id INTEGER PRIMARY KEY,name TEXT,data BLOP,date TEXT)""")
    cursor.execute("""INSERT INTO FilesTbl (name, data, date) VALUES (?,?,datetime('now'))""",(file_name, file_data))

    conn.commit()
    cursor.close()
    conn.close()

def file_init(row_data):
    file = Files()
    file.file_id = row_data["file_id"]
    file.data = BytesIO(row_data["data"])
    file.name = row_data["name"]
    file.date = row_data["date"]
    return  file

#CLASSES
class Files:
    def __init__(self):
        self.file_id = 0
        self.name = ""
        self.data = ""
        self.date = ""


if __name__ == "__main__":
    app.run(debug=True)