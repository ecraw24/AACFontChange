from distutils.log import debug
from fileinput import filename
from flask import * 
import os
from werkzeug.utils import secure_filename
import Unzip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))) 
        Unzip.extractDB(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return render_template("uploadSuccess.html", name = f.filename)  

if __name__ == "__main__":
  app.run()