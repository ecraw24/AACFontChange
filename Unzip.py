import os
import zipfile
import shutil

rawFile = 'WordPower60 SS.ce'
base = os.path.splitext(rawFile)[0]
shutil.copy(rawFile, 'WordPower60 SS - copy.ce')
fileCopy = 'WordPower60 SS - copy.ce'
os.rename(fileCopy, base + '.zip')
zipFile = 'WordPower60 SS.zip'

with zipfile.ZipFile(zipFile, 'r') as zip_ref:
    zip_ref.extractall(os.getcwd())

rawFile = 'WordPower60 SS_Copy.c4v'
base = os.path.splitext(rawFile)[0]
shutil.copy(rawFile, 'WordPower60 SS - copy2.c4v')
fileCopy = 'WordPower60 SS - copy2.c4v'
os.rename(fileCopy, base + '.db')
dbFile = 'WordPower60 SS.db'




