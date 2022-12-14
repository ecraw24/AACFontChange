# loading in modules
import sqlite3

def printTables (dbFilePath):
    # creating file path
    #dbfile = r'C:\Users\wydnerk\OneDrive\Personal\My Projects\AACFileChanger\WordPower60 SS\WordPower60 SS_Copy.db'
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(dbFilePath)
    print(dbFilePath)

    # creating cursor
    cur = con.cursor()

    # reading all table names
    #table_list = [a for a in cur.execute("SELECT * FROM button_styles")]
    table_list = [a for a in cur.execute("SELECT name from sqlite_master where type= 'table'")]
    #table_list = cur.fetchall()
    #(table_list)

    # here is you table list
    #print(table_list)

    # Be sure to close the connection
    con.close()

    return table_list