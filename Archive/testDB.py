# loading in modules
import sqlite3

# Create a SQL connection to our SQLite database
dbFilePath = "FinalTimesTest.db"

con = sqlite3.connect(dbFilePath)
print(dbFilePath)

# creating cursor
cur = con.cursor()

# reading all table names
#[a for a in cur.execute("update button_styles set font_name='Times' where font_name='Ubuntu'")]
table_list = [a for a in cur.execute("SELECT * from button_styles")]
print(table_list)
# Be sure to close the connection
con.close()



