import sqlite3


# --------CREATING A TABLE-------
def create_acc_table():
    conn = sqlite3.connect("acc_info.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE acc_info(
                acc_no integer,
                name text,
                balance integer,
                acc_type text
            )"""
    )
    conn.commit()
    conn.close()


def create_transac_table():
    conn = sqlite3.connect("transaction.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE acc_info(
                creditor text,
                debitor text,
                amount integer,
                timestamp text,
                remark text
            )"""
    )
    conn.commit()
    conn.close()


# --------INSERTING RECORDS/ENTRIES IN TABLE-------
def insert_acc(acc_list):
    conn = sqlite3.connect("acc_info.db")
    c = conn.cursor()
    c.executemany("INSERT INTO acc_info VALUES(?, ?, ?, ?)", acc_list)
    conn.commit()
    conn.close()


def insert_transac(transac_list):
    conn = sqlite3.connect("transaction.db")
    c = conn.cursor()
    c.executemany("INSERT INTO acc_info VALUES(?, ?, ?, ?, ?)", transac_list)
    conn.commit()
    conn.close()


# --------FETCHING RECORDS FROM TABLE-------
def fetch_all_acc():
    conn = sqlite3.connect("acc_info.db")
    c = conn.cursor()
    print(c.fetchall())
    # entries = c.fetchall()
    # for entry in entries:
    #     print(entry)
    conn.commit()
    conn.close()


def fetch_all_transac():
    conn = sqlite3.connect("transaction.db")
    c = conn.cursor()
    print(c.fetchall())
    # entries = c.fetchall()
    # for entry in entries:
    #     print(entry)
    conn.commit()
    conn.close()


# --------FETCHING RECORDS FROM TABLE-------
def fetch():
    conn = sqlite3.connect("acc_info.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM acc_info")
    c.execute(
        "SELECT rowid, * FROM acc_info WHERE name like '%ArYa'"
    )  # Case-Insensitive
    print(c.fetchone())
    print(c.fetchmany(2))
    print(c.fetchall())
    entries = c.fetchall()
    for entry in entries:
        print(entry)
    conn.commit()
    conn.close()


# --------FETCHING RECORDS FROM TABLE-------

# c.execute("UPDATE acc_info SET name = 'Flick Arya' WHERE rowid = 2")
# c.execute("SELECT rowid, * FROM acc_info")
# c.execute("SELECT rowid, * FROM acc_info ORDER BY NAME ASC")
# c.execute("SELECT rowid, * FROM acc_info ORDER BY ROWID DESC")
# entries = c.fetchall()
# for entry in entries:
#     print(entry)


# --------DELETING RECORDS FROM TABLE-------
def delete_acc():
    conn = sqlite3.connect("acc_info.db")
    c = conn.cursor()
    # c.execute("DELETE FROM acc_info WHERE rowid = 2")
    # c.execute("SELECT rowid, * FROM acc_info")
    # entries = c.fetchall()
    # for entry in entries:
    #     print(entry)
    conn.commit()
    conn.close()


def delete_transac():
    conn = sqlite3.connect("transaction.db")
    c = conn.cursor()
    # c.execute("DELETE FROM acc_info WHERE rowid = 2")
    # c.execute("SELECT rowid, * FROM acc_info")
    # entries = c.fetchall()
    # for entry in entries:
    #     print(entry)
    conn.commit()
    conn.close()


# --------DELETING RECORDS FROM TABLE-------
def delete_acc_table():
    conn = sqlite3.connect("acc_info.db")
    c = conn.cursor()
    c.execute("DROP TABLE acc_info")
    conn.commit()
    conn.close()


def delete_transac_table():
    conn = sqlite3.connect("transaction.db")
    c = conn.cursor()
    c.execute("DROP TABLE transacton")
    conn.commit()
    conn.close()
