import sqlite3
from sqlite3 import Error

def connection(path:str):
    try:
        con = sqlite3.connect(path)
        return con
    except Error:
        print('Error')

con = connection('tree.db')
sql = """CREATE TABLE "TREE" (
	"node_id"	TEXT NOT NULL,
	"state"	TEXT NOT NULL,
	"player"	INTEGER NOT NULL,
	"child"	TEXT NOT NULL,
	"parent"	TEXT NOT NULL,
	"win"	INTEGER NOT NULL,
	"visit"	INTEGER NOT NULL
);"""
cur = con.cursor()
cur.execute(sql)
con.commit()

con.close()
