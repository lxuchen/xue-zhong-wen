import sqlite3
from datetime import date


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def create_table(table_name, database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute("CREATE TABLE " + table_name + " (char text, pinyin text, display integer, mark integer)")

    conn.commit()
    conn.close()

def delete_table(table_name, database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute("DROP TABLE " + table_name)

    conn.commit()
    conn.close()

def create_schedule(table_name, database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute("CREATE TABLE " + table_name + " (date text, day text, cards text, number text)")

    conn.commit()
    conn.close()

def insert_schedule(dt, dy, cd, nb, table_name, database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute( "INSERT INTO " + table_name + " VALUES (:d, :dd, :c, :n)",
        {
            'd':dt,
            'dd':dy,
            'c':cd,
            'n':nb
        })

    conn.commit()
    conn.close()

def insert_record(cc, py, dis, ma, table_name, database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute( "INSERT INTO " + table_name + " VALUES (:c, :p, :d, :m)",
        {
            'c':cc,
            'p':py,
            'd':dis,
            'm':ma
        })

    conn.commit()
    conn.close()

def query_all(table_name, database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute( "SELECT *, oid from " + table_name)
    print(c.fetchall())

    conn.commit()
    conn.close()

def delete_record(id, table_name, database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute( "DELETE from " + table_name + " WHERE oid = " + str(id))
    print(c.fetchall())

    conn.commit()
    conn.close()




# delete_table("words", "Chinese.db")
# create_table("words1000", "Chinese.db")
# create_table("words2000", "Chinese.db")
# create_table("words3000", "Chinese.db")
# create_table("words_all", "Chinese.db")


# with open('Chinese1000.txt') as f:
#     lines = [line.rstrip() for line in f]

# for i in lines:
#     insert_record(i.split(":")[0], i.split(":")[1], 1, 0, "words1000", "Chinese.db")

# with open('Chinese2000.txt') as f:
#     lines = [line.rstrip() for line in f]

# for i in lines:
#     insert_record(i.split(":")[0], i.split(":")[1], 1, 0, "words2000", "Chinese.db")

# with open('Chinese3000.txt') as f:
#     lines = [line.rstrip() for line in f]

# for i in lines:
#     insert_record(i.split(":")[0], i.split(":")[1], 1, 0, "words3000", "Chinese.db")

# with open('ChineseAll.txt') as f:
#     lines = [line.rstrip() for line in f]

# for i in lines:
#     insert_record(i.split(":")[0], i.split(":")[1], 1, 0, "words_all", "Chinese.db")

# delete_table("schedule", "Chinese.db")
# create_schedule("schedule", "Chinese.db")

# with open('Schedules.txt') as f:
#     lines = [line.rstrip() for line in f]

# for i in lines:
#     if(i.split(":")[2] != "break"):
#         insert_schedule(i.split(":")[0], i.split(":")[1], i.split(":")[2], i.split(":")[3], "schedule", "Chinese.db")
#     else:
#         insert_schedule(i.split(":")[0], i.split(":")[1], i.split(":")[2], 0, "schedule", "Chinese.db")

# query_all("schedule", "Chinese.db")
# query_all("words1000", "Chinese.db")

