from distutils.log import debug
from fileinput import filename
from flask import * 
import os
from werkzeug.utils import secure_filename
from Scripts import file_manipulator, sql
import shutil
import tempfile 
import atexit

app = Flask(__name__)

#global variables
fonts = ['Amaranth', 'Arial', 'Caudex', 'Courier New', 'Frutiger Linotype', 'Gentium Basic', 'Georgia', 'Istok Web', 
                'Josefin Sans', 'Puritan', 'Tahoma', 'Times New Roman', 'Trebuchet MS', 'Ubuntu', 'Verdana']
tmpdirname = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=os.getcwd()) #change to dir in pythonAnywhere
dbFilePath = tmpdirname.name + '\\temp.db'

def clearTmpFolder(tmpFolder):
  folder = tmpFolder
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
          os.unlink(file_path)
      elif os.path.isdir(file_path):
          shutil.rmtree(file_path)
    except Exception as e:
      print('Failed to delete %s. Reason: %s' % (file_path, e))

### START ROUTES ###

@app.route('/')
def index():
  clearTmpFolder(tmpdirname.name)
  return render_template('index.html')

@app.route('/fontHome', methods=['POST', 'GET'])
def fontHome():
  clearTmpFolder(tmpdirname.name)
  return render_template('fontHome.html')

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        
        #get file and create tmp dir
        f = request.files['file']
        #save file to directory and extract; if not, cleanup temp folder
        try: 
          FilePath = os.path.join(tmpdirname.name, secure_filename(f.filename))
          f.save(FilePath) 
          file_manipulator.extractDB(FilePath, tmpdirname.name)
        except:
          print('extract failed')
          clearTmpFolder(tmpdirname.name)
        
        return render_template("uploadSuccess.html", fonts=fonts, complete='')  

@app.route('/fontChange', methods = ['POST', 'GET'])
def fontChange():
  source = list(request.form.keys())[0] #export, import, or font change
  
  if request.method == 'POST':
    try:
      print('directory for temp.db: ' + tmpdirname.name)
      if source == 'fontChange':
        sql.changeFonts(request.form['fontFrom'], request.form['fontTo'], tmpdirname.name)
      if source == 'fontSizeChange':
        sql.changeFontSize(request.form['fontFrom'], request.form['fontTo'], tmpdirname.name)
    except:
      print('font change failed')
      clearTmpFolder(tmpdirname.name)
    return render_template("downloadFile.html")

@app.route('/download', methods=['POST', 'GET'])
def download():
  source = list(request.form.keys())[0] #export, import, or font change
  print('source: ', list(request.form.keys()))
 
  if source == 'UploadCEForPages':
    #get file and create tmp dir
    f = request.files['file']
    #save file to directory and extract; if not, cleanup temp folder
    try: 
      FilePath = os.path.join(tmpdirname.name, secure_filename(f.filename))
      f.save(FilePath) 
      file_manipulator.extractDB(FilePath, tmpdirname.name)
      pages = sql.getPages(tmpdirname.name)
      return render_template('bulkEditHome.html', pages=pages, alert='Upload successful!')
    except:
      print('error in uploadCEForPages')

  if ('Export' in list(request.form.keys())):  
    try: 
      csvPath = sql.getExport(tmpdirname.name, request.form['page'] )
      return send_file(csvPath, as_attachment=True)  
    except:
      print('extract failed')
      clearTmpFolder(tmpdirname.name)
  
  if source == 'Import':  
    #get file and create tmp dir
    f = request.files['file']
    #save file to directory and extract; if not, cleanup temp folder
    try: 
      FilePath = os.path.join(tmpdirname.name, secure_filename(f.filename))
      f.save(FilePath) 
      sql.importCSV(FilePath, tmpdirname.name)
      zipFilePath = [os.path.join(tmpdirname.name, file) for file in os.listdir(tmpdirname.name) if file.endswith('.zip')]
      newCEPath = file_manipulator.rezipDB(dbFilePath, zipFilePath[0], tmpdirname.name)
      alert='csv import complete'
      return send_file(newCEPath, as_attachment=True) 
    except:
      print('import failed')
      clearTmpFolder(tmpdirname.name)

  if source == 'fontChange':  
    try:
      zipFilePath = [os.path.join(tmpdirname.name, file) for file in os.listdir(tmpdirname.name) if file.endswith('.zip')]
      newCEPath = file_manipulator.rezipDB(dbFilePath, zipFilePath[0], tmpdirname.name)
      alert='font change complete'
      return send_file(newCEPath, as_attachment=True)   
    except:
      print('rezip or download failed')
      clearTmpFolder(tmpdirname.name)
  
  alert='error: you fucked up'
  return render_template('index.html', alert=alert)

@app.route('/bulkEdit', methods = ['POST', 'GET'])
def bulkEditHome():
  clearTmpFolder(tmpdirname.name)
  return render_template('bulkEditHome.html')

@app.route('/bulkUploadSuccess')
def bulkUploadSuccess():  
    if request.method == 'POST':  
        
        #get file and create tmp dir
        f = request.files['file']
        
        #save file to directory and extract; if not, cleanup temp folder
        #try: 
        FilePath = os.path.join(tmpdirname.name, secure_filename(f.filename))
        f.save(FilePath) 
        file_manipulator.extractDB(FilePath, tmpdirname.name)
        #except:
          #print('extract failed')
          #clearTmpFolder(tmpdirname.name)
        
        return render_template("uploadSuccess.html", fonts=fonts, complete='')

### END ROUTES ###

def OnExitApp():
    tmpdirname.cleanup()

atexit.register(OnExitApp)

if __name__ == "__main__":
  app.run()
