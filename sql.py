# loading in modules
import sqlite3

# creating file path
dbfile = r'C:\Users\wydnerk\OneDrive\Personal\My Projects\AACFileChanger\WordPower60 SS\WordPower60 SS_Copy.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
table_list = [a for a in cur.execute("SELECT * FROM button_styles")]
# here is you table list
print(table_list)

# Be sure to close the connection
con.close()