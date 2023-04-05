import numpy as np
import sqlite3
from sqlite3 import Error
import ast
from MCTS_NodeDrop import MCTF
mctf = MCTF()

tree = mctf.load_tree('db_test.txt')
# print(tree)

def connection(path:str):
    try:
        con = sqlite3.connect(path)
        return con
    except Error:
        print('Error')

con = connection('tree.db')


def update_data(con, data):
    try:
        cur = con.cursor()
        # sql = "UPDATE TREE SET node_id=?, state=?, player=?, child=?, parent=?, win=?, visit=? Where ID = ?"
        sql = "INSERT INTO TREE VALUES(?,?,?,?,?,?,?)"
        cur.execute(sql, data)
        con.commit()
    except Exception as e: print('Error :', e)

def read_all(con):
    try:
        cur = con.cursor()
        sql = "SELECT * FROM TREE"
        cur.execute(sql)
        data = cur.fetchall()
        return data
    except Exception as e: print('Error :', e)

def delete_all(con):
    try:
        cur = con.cursor()
        sql = 'DELETE FROM TREE;'
        cur.execute(sql)
        con.commit()
    except Exception as e: print('Error :', e)

# _tree = read_all(con)
delete_all(con)

for _id in tree:
    node_id = _id
    state = list(tree[node_id]['state'].flatten())
    player = tree[node_id]['player']
    child = tree[node_id]['child']; parent = tree[node_id]['parent']
    win = tree[node_id]['win']; visit = tree[node_id]['visit']
    data = (str(node_id), str(state), player, str(child), str(parent), win, visit)
    # print(data)
    update_data(con, data)
    # print(state, player, child, parent, win, visit)

# cur.execute("INSERT INTO TREE VALUES (2, '(1,2,3,4,5)')")

# Save (commit) the changes
# con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
_tree = read_all(con)
for _data in _tree:
    node_id, state, player, child, parent, win, visit = _data
    print(np.array(ast.literal_eval(state), dtype=np.int32).reshape((6,7)))
con.close()
