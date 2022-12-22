# loading in modules
import sqlite3
import os
import csv


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

def changeFontSize(fontFrom, fontTo, tmpdirpath):
    con = sqlite3.connect(os.path.join(tmpdirpath, "temp.db"))
    cur = con.cursor()
    print('fontFrom: ', fontFrom, '; fontTo: ', fontTo)

    cur.execute("update button_styles set font_height=" + fontTo + " where font_height=" + fontFrom)

    con.commit()
    con.close()

def getExport(tmpdirpath):

    try:
        con = sqlite3.connect(os.path.join(tmpdirpath, "temp.db"))
        cur = con.cursor()

        select = '''Select
                        bbc.resource_id,
                        r.name AS page_name,
                        b.label, b.message

                    FROM button_box_cells bbc
                        LEFT JOIN buttons b ON b.resource_id = bbc.resource_id
                        LEFT JOIN button_box_instances bbi ON bbi.button_box_id = bbc.button_box_id
                        LEFT JOIN pages p ON p.id = bbi.page_id
                        LEFT JOIN resources r ON r.id = p.resource_id

                    WHERE b.visible=1
                    ORDER BY page_name
                    LIMIT 10;'''

        cur.execute(select)
        csvPath = os.path.join(tmpdirpath, "EditVocabulary.csv")
        with open(csvPath, 'w',newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)
        return csvPath

    except:
        print('export failed')
    finally:
        con.close()


def importCSV(csvFilePath, tmpdirpath):
    try:
        con = sqlite3.connect(os.path.join(tmpdirpath, "temp.db"))
        cur = con.cursor()
        # Import csv and extract data
        with open(csvFilePath, 'r') as fin:
            dr = csv.DictReader(fin)
            contents = [(i['label'], i['message'], i['resource_id']) for i in dr]
            print(contents)
        update = '''UPDATE buttons
                    SET label = ? ,
                        message = ?
                    WHERE resource_id = ?'''
        cur.executemany(update, contents)
        con.commit()
    except:
        print('import error')
    finally:
        con.close()
