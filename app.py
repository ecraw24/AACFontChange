from distutils.log import debug
from fileinput import filename
from flask import * 
import os
from werkzeug.utils import secure_filename
import Unzip
import sql
import shutil 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads/'
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
fonts = ['Amaranth', 'Arial', 'Caudex', 'Courier New', 'Frutiger Linotype', 'Gentium Basic', 'Georgia', 'Istok Web', 
                'Josefin Sans', 'Puritan', 'Tahoma', 'Times New Roman', 'Trebuchet MS', 'Ubuntu', 'Verdana']

@app.route('/', methods=['GET'])
def index():
    #if request.method == 'GET':
    folder = 'extractedDBs' 
    for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
      except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
    folder = 'Uploads' 
    for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
      except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    return render_template('index.html')

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        FilePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(FilePath) 
        dbFilePath = Unzip.extractDB(FilePath)
        tableList = sql.printTables(dbFilePath)
        
        return render_template("uploadSuccess.html", name = dbFilePath, table=tableList, fonts=fonts, complete='')  

@app.route('/fontChange', methods = ['POST', 'GET'])
def fontChange():
  if request.method == 'POST':
    sql.changeFonts(request.form['fontFrom'], request.form['fontTo'], 'extractedDBs\WordPower60 SS_Copy.db')
    return render_template("downloadFile.html")

@app.route('/download')
def download():
    path = 'extractedDBs\WordPower60 SS_Copy.db'
    return send_file(path, as_attachment=True)   

if __name__ == "__main__":
  app.run()