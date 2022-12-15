# loading in modules
import sqlite3
import os

def printTables (dbFilePath):
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(dbFilePath)
    print(dbFilePath)

    # creating cursor
    cur = con.cursor()

    # reading all table names
    table_list = [a for a in cur.execute("SELECT name from sqlite_master where type= 'table'")]

    # Be sure to close the connection
    con.close()

    return table_list

#def changeFonts(fontFrom, fontTo, dbFilePath):
def changeFonts(fontFrom, fontTo, tmpdirpath):
    print('used for connection string: ' + os.path.join(tmpdirpath, "temp.db"))
    con = sqlite3.connect(os.path.join(tmpdirpath, "temp.db"))
    cur = con.cursor()

    #updateString = "update button_styles set font_name='" + fontTo + "' where font_name='" + fontFrom + "'"
    #print(updateString)
    cur.execute("update button_styles set font_name='" + fontTo + "' where font_name='" + fontFrom + "'")
    #test = [a for a in cur.execute("SELECT * from button_styles")]
    #print(test)
    con.commit()
    con.close()
