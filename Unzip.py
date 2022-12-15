import os
import zipfile
import shutil
import pathlib

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
    
    #convert from db to c4v
    os.rename(dbFilePath, 'temp.c4v')
    
    with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
        zip_ref.extractall(path=tmpdirpath + '\\tmpDir')
        zip_ref.close()
    
    #get the original name of the c4v file extracted from zip
    c4vOriginalName = [os.path.join(tmpdirpath + '\\tmpDir', file) for file in os.listdir(tmpdirpath + '\\tmpDir') if file.endswith('.c4v')]
    zipOriginalName = [os.path.join(tmpdirpath, file) for file in os.listdir(tmpdirpath) if file.endswith('.zip')]
    print(zipOriginalName[0])
    
    #rename temp file to new c4v file and delete old c4v
    os.rename('temp.c4v', os.path.splitext(c4vOriginalName[0])[0] + '-NEW.c4v')
    os.remove(c4vOriginalName[0])
    
    #take original name of zip file and add new, remove old zip, and create new archive
    baseZip = os.path.splitext(zipOriginalName[0])[0] + '-NEW.zip'
    print(baseZip)
    directory = pathlib.Path(tmpdirpath + "/tmpDir/")

    with zipfile.ZipFile(baseZip, mode="w") as archive:
        for file_path in directory.iterdir():
            archive.write(file_path, arcname=file_path.name)

    print('archive created')
    print(baseZip)
    return (baseZip)


