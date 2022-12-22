import os
import zipfile
import shutil
import pathlib

def extractDB(inputFilePath, tmpdirname):

    base = os.path.splitext(inputFilePath)[0]
    zipFile = base + '.zip'

    print('inputpath: ' + inputFilePath +', zipFilePath: ' + zipFile)

    os.rename(inputFilePath, zipFile)

    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
        extractedc4v = [zip_ref.extract(file, tmpdirname) for file in zip_ref.namelist() if file.endswith('.c4v')]
        zip_ref.close()

    print(extractedc4v[0])

    for file in extractedc4v:
        print('file extraction: ', file)
        print('rename to: ', os.path.join(tmpdirname, 'temp.db'))
        os.rename(file, os.path.join(tmpdirname, 'temp.db'))
    print('extract db successful')

def rezipDB(dbFilePath, zipFilePath, tmpdirpath):

    #convert from db to c4v
    os.rename(dbFilePath, tmpdirpath + '/temp.c4v')
    print('dbfilepath: ' + dbFilePath)
    print(zipFilePath)
    print('new db file path: ' + tmpdirpath + '/temp.c4v')

    #extract files to tmpDir
    with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
        zip_ref.extractall(path=tmpdirpath + '/tmpDir')
        zip_ref.close()

    #get the original name of the c4v file extracted from zip
    c4vOriginalName = [os.path.join(tmpdirpath + '/tmpDir', file) for file in os.listdir(tmpdirpath + '/tmpDir') if file.endswith('.c4v')]
    zipOriginalName = [os.path.join(tmpdirpath, file) for file in os.listdir(tmpdirpath) if file.endswith('.zip')]

    #rename temp file to new c4v file and delete old c4v
    shutil.move(tmpdirpath + '/temp.c4v', tmpdirpath + '/tmpDir/')
    os.rename(os.path.join(tmpdirpath, 'tmpDir/temp.c4v'), os.path.splitext(c4vOriginalName[0])[0] + '-NEW.c4v')
    os.remove(c4vOriginalName[0])

    #take original name of zip file and add new, remove old zip, and create new archive
    baseZip = os.path.splitext(zipOriginalName[0])[0] + '-NEW.zip'
    directory = pathlib.Path(tmpdirpath + "/tmpDir/")

    with zipfile.ZipFile(baseZip, mode="w") as archive:
        for file_path in directory.iterdir():
            archive.write(file_path, arcname=file_path.name)

    os.rename(os.path.splitext(zipOriginalName[0])[0] + '-NEW.zip', os.path.splitext(zipOriginalName[0])[0] + '-NEW.ce',)
    CEFilePath = os.path.splitext(zipOriginalName[0])[0] + '-NEW.ce'
    return (CEFilePath)


