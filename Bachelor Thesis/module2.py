import sqlite3
import pandas as pd
import numpy as np

def db_interface():
    
    # makes a connection object to the data base
    conn = sqlite3.connect('Auswertung_DB.sqlite')
    # makes a cursor in order to perform operations
    cur = conn.cursor()
    # Feedback message
    print("Successfully connected to the data base!\n")

    # Displaying dictionary of the tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    all_tables = np.array(cur.fetchall())
    d = dict(enumerate(all_tables.flatten(), 1))
    for k, v in d.items():
        print(k, ' : ', v)

    key = int(input("Select from available TABLES:\n"))
    print(f"\n'{d[key]}' selected:")
    df = get_table(d[key], conn)
    print(df)
    
    ans = input("PRESS '0' to add NULL-POINTS or ENTER to CONTINUE:\n")
    if ans == '0':
        for i in range(len(df)): 
            insert_np(cur, conn, d[key], i+1)
            
        df_updated = get_table(d[key], conn)
        conn.close()
        return df_updated, d[key]
    else:
        return df, d[key]


# creates new table
def create_new_table(cur, conn, table_name):
    # creates table with input name
    create_table_query = f'''
                         CREATE TABLE IF NOT EXISTS {table_name} (
                                start_times DATETIME,
                                temperature INTEGER,
                                null_point INTEGER,
                                time_to_0x005_Pa INTEGER,
                                time_to_0x01_Pa INTEGER,
                                time_to_0x05_Pa INTEGER
                                )
                         '''
    cur.execute(create_table_query)
    conn.commit()
    

# inserts start times and temperature into the table
def insert_items(cur, conn, table_name):
    count = int(input("Enter the number of data samples:\n"))
    print("Enter data samples")
    for i in range(1, count+1):
        start_time, temp = input().split()
        insert_query = f'INSERT INTO {table_name} (start_times, temperature) VALUES (?, ?)'
        cur.execute(insert_query, (start_time, temp))
        conn.commit()
        
        
# inserts null_points into the table
def insert_np(cur, conn, table_name, index):
    null_point = input("Enter NULL-POINT: ")
    insert_query = f'''
                    UPDATE {table_name} 
                    SET null_point = ? 
                    WHERE rowid ==  ?
                    '''
    cur.execute(insert_query, (null_point, index))
    conn.commit()
    
    
# inserts times into the table
def insert_time(cur, conn, table_name, t1, time, t3, index):
    insert_query = f'''
                    UPDATE {table_name}
                    SET 
                    time_to_0x01_Pa = ?,
                    time_to_0x005_Pa = ?,
                    time_to_0x05_Pa = ?
                    WHERE 
                    rowid ==  ?
                    '''
    cur.execute(insert_query, (time, t1, t3, index))
    conn.commit()
        

# returns a table as dataframe
def get_table(table_name, conn):
    # saves table as dataframe
    get_table_query = f'SELECT * from {table_name}'
    df = pd.read_sql_query(get_table_query, conn)
    
    return df


def update_table():
    pass


def add_columns(table_name, cur, conn):
    rename_table_query = f"ALTER TABLE {table_name} RENAME TO TempOldTable;"
    cur.execute(rename_table_query)
    conn.commit()
    
    create_new_table_query = f"""CREATE TABLE {table_name} (
                                start_times DATETIME,
                                temperature INTEGER,
                                null_point INTEGER,
                                time_to_0x005_Pa INTEGER,
                                time_to_0x01_Pa INTEGER,
                                time_to_0x05_Pa INTEGER
                                )"""
    cur.execute(create_new_table_query)
    conn.commit()
    
    populate_new_table_query = f"""INSERT INTO {table_name} (
                                    start_times,
                                    temperature,
                                    null_point,
                                    time_to_0x01_Pa
                                    )
                                    SELECT start_times, temperature, null_point, time_in_seconds FROM TempOldTable"""
    cur.execute(populate_new_table_query)
    conn.commit()
    
    delete_old_table_query = "DROP TABLE TempOldTable;"
    cur.execute(delete_old_table_query)
    conn.commit()


def update_columns():
    conn = sqlite3.connect('Auswertung_DB.sqlite')

    cur = conn.cursor()

    print("Successfully connected to the data base!\n")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    all_tables = np.array(cur.fetchall())
    d = dict(enumerate(all_tables.flatten(), 1))
    for k, v in d.items():
        print(k, ' : ', v)

    key = int(input("Select from available TABLES to modify:\n"))
    print(f"\n'{d[key]}' selected:")
    df = get_table(d[key], conn)
    print(df)
    
    add_columns(d[key], cur, conn)
    print(get_table(d[key], conn))
    conn.close()