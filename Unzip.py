import os
import zipfile
import shutil

def extractDB(inputFilePath):
    base = os.path.splitext(inputFilePath)[0]
    newName = base + '- NewExtension' + '.ce'
    shutil.copy(inputFilePath, newName)
    os.rename(newName, base + '.zip')
    zipFile = base + '.zip'
    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
        extractedc4v = [zip_ref.extract(file, 'extractedDBs/') for file in zip_ref.namelist() if file.endswith('.c4v')]
        zip_ref.close()
    os.remove(zipFile)
    print(extractedc4v)
    for inputFilePath in extractedc4v:
        base = os.path.splitext(inputFilePath)[0]
        newName = inputFilePath + '- NewUnzip' + '.c4v'
        shutil.copy(inputFilePath, newName)
        os.rename(newName, base + '.db')
        os.remove(inputFilePath)
    dbFilePath = base + '.db'
    print(dbFilePath)
    return dbFilePath




