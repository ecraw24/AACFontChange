# loading in modules
import sqlite3

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

def changeFonts (fontFrom, fontTo, dbFilePath):
    con = sqlite3.connect(dbFilePath)
    print(dbFilePath)
    cur = con.cursor()

    [a for a in cur.execute("update button_styles set font_name='" + fontTo + "' where font_name='" + fontFrom + "'")]

    con.close()
