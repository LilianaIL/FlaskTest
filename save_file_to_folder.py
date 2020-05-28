from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.curdir+'/static/documents/'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif','docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print(file)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('home.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == "__main__":
    app.run(debug=True)