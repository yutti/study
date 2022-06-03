import sqlite3

def make_table(cur):
    # make the table
    cur.execute(
        'CREATE TABLE bookitems(name TEXT , code INTEGER, status INTEGER)'
    )
    
    # Data registration
    inserts = [
        ("あいうえお",10001, 0),
        ("かきくけこ",10002, 0),
        ("さしすせそ",10003, 0),
        ("たちつてと",10004, 0),
        ("なにぬねの",10005, 0),
        ("はひふへほ",10006, 0),
        ("まみむめも",10007, 0),
        ("やゆよ",10008, 0),
        ("らりるれろ",10009, 0),
        ("わをん",10010, 0)
    ]
    # execute many data 
    cur.executemany('INSERT INTO bookitems values(?, ?, ?)', inserts)

    # print table data
    # cur.execute('SELECT * FROM bookitems')
    #for row in cur:
    #    print(row)

    cur.close()
    
def reset_status(cur):
    cur.execute('UPDATE bookitems SET status = "0" ')
    cur.close()    

def main():
    
    # connect database
    dbname = 'book_list.db'
    conn = sqlite3.connect(dbname)
    # make cursor to operate SQlite
    cur = conn.cursor()
    #get the count of tables with the name
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookitems' ''')
    if cur.fetchone()[0]==1:
        reset_status(cur)
    else:
        make_table(cur)
    conn.commit()   # commit 
    conn.close()    # close data base

if __name__ == '__main__':
    main()