from distutils.log import debug
from fileinput import filename
from flask import * 
import os
from werkzeug.utils import secure_filename
import Unzip
import sql
import shutil
import tempfile 

app = Flask(__name__)
fonts = ['Amaranth', 'Arial', 'Caudex', 'Courier New', 'Frutiger Linotype', 'Gentium Basic', 'Georgia', 'Istok Web', 
                'Josefin Sans', 'Puritan', 'Tahoma', 'Times New Roman', 'Trebuchet MS', 'Ubuntu', 'Verdana']
tmpdirname = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=os.getcwd())
dbFilePath = tmpdirname.name + '\\temp.db'


@app.route('/', methods=['POST', 'GET'])
def index():
    #clear tmp folder
    folder = tmpdirname.name 
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
        
        #get file and create tmp dir
        f = request.files['file']
        
        #save file to directory and extract; if not, cleanup temp folder
        try: 
          FilePath = os.path.join(tmpdirname.name, secure_filename(f.filename))
          f.save(FilePath) 
          Unzip.extractDB(FilePath, tmpdirname.name)
          tableList = sql.printTables(dbFilePath)
        except:
          print('extract failed')
          tmpdirname.cleanup()
        
        return render_template("uploadSuccess.html", table=tableList, fonts=fonts, complete='')  

@app.route('/fontChange', methods = ['POST', 'GET'])
def fontChange():
  if request.method == 'POST':
    try:
      print('directory for temp.db: ' + tmpdirname.name)
      sql.changeFonts(request.form['fontFrom'], request.form['fontTo'], tmpdirname.name)
    except:
      print('try failed')
      tmpdirname.cleanup()
    return render_template("downloadFile.html")

@app.route('/download')
def download():
    try:
      zipFilePath = [os.path.join(tmpdirname.name, file) for file in os.listdir(tmpdirname.name) if file.endswith('.zip')]
      newCEPath = Unzip.rezipDB(dbFilePath, zipFilePath[0], tmpdirname.name)
      return send_file(newCEPath, as_attachment=True)   
    except:
      print('rezip or download failed')
      tmpdirname.cleanup()
    return render_template('index.html')

if __name__ == "__main__":
  app.run()
