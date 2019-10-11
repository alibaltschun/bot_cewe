import sqlite3


def __create_table__():
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE rating
                 (username text , id_cewe integer, rate interger,
                 UNIQUE(username, id_cewe) ON CONFLICT REPLACE)''')
    
    conn.commit()
    conn.close()
    
def __rate_cewe__(name,id_cewe,rate):
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    c.execute("insert or replace into rating values('{}',{},{})".format(name,id_cewe,rate))
    
    conn.commit()
    conn.close()
    
def __get_rated__(id_cewe):
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    rows = []
    for row in c.execute('''select rate,group_concat(username, ",") from rating
                         where id_cewe={}
                         group by rate'''.format(id_cewe)):
        rows.append(row)
    conn.commit()
    conn.close()
    
    return rows
    
def __select_all_rating__():
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    rows = []
    for row in c.execute('select * from rating'):
        rows.append(row)
        
    conn.close()
    return rows


def __get_cewe_unvoted__(username):
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    rows = []
    for row in c.execute('''select id_cewe from rating
                         where username="{}"'''.format(username)):
        rows.append(row)
        
    conn.commit()
    conn.close()
    
    # get smallest id cewe that not been voted by user
    rows = [i[0] for i in rows]
    n = len([name for name in os.listdir("."+STATIC) if os.path.isfile("."+STATIC+"/"+name)])
    id_cewe = list(set([i for i in range(n)])-set(rows))
    id_cewe = -1 if id_cewe == [] else id_cewe
    
    return id_cewe
    