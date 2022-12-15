import os
import zipfile
import shutil

def extractDB(inputFilePath, tmpdirname):
    base = os.path.splitext(inputFilePath)[0]
    newName = base + '- NewExtension' + '.ce'
    shutil.copy(inputFilePath, newName)
    os.rename(newName, base + '.zip')
    zipFile = base + '.zip'
    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
        extractedc4v = [zip_ref.extract(file, tmpdirname) for file in zip_ref.namelist() if file.endswith('.c4v')]
        zip_ref.close()
    os.remove(inputFilePath)
    for inputFilePath in extractedc4v:
        base = os.path.splitext(inputFilePath)[0]
        newName = inputFilePath + '- NewUnzip' + '.c4v'
        shutil.copy(inputFilePath, newName)
        os.rename(newName, tmpdirname + '\\' + 'temp.db')#'extractedDBs\\temp.db')
        os.remove(inputFilePath)
    print('extract db successful')

def rezipDB(dbFilePath, zipFilePath, tmpdirpath):
    baseDB = os.path.splitext(dbFilePath)[0]
    baseZip = os.path.splitext(zipFilePath)[0] + '-NEW'
    os.rename(dbFilePath, baseDB + '.c4v')
    #zipfile.ZipFile(zipFilePath, 'r').extractall()
    with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
        zip_ref.extractall()
        zip_ref.close()
    c4vOriginalName = [file for file in os.getcwd() if file.endswith('.c4v')]
    print(c4vOriginalName)
    os.remove(c4vOriginalName)
    os.rename(dbFilePath, c4vOriginalName)
    shutil.make_archive(baseZip, format='zip', root_dir=tmpdirpath)
    print(baseZip + '.zip')
    return baseZip + '.zip'


