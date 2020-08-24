import sqlite3
import numpy as np
import pandas as pd


DB_FILE = 'MoneyManagerBackup'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    # TODO: Used connection pools
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def get_raw_data():
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    # TODO: Sanitize queries
    query_string = '''
                    SELECT  assetUID, categoryUID, ZMONEY, DO_TYPE, WDATE
                    FROM INOUTCOME 
                    ORDER BY ZDATE ;
                    '''
    cur.execute(query_string)

    rows = cur.fetchall()
    conn.close()
    return rows

def create_running_balance(data):
    ''' DO_TYPE
        0 = Income
        1 = Expenses
        3 = Tranfer
        4 = Savings/Investments
    '''
    columns = ['assetUID', 'categoryUID', 'ZMONEY', 'DO_TYPE', 'WDATE']
    df = pd.DataFrame(data, columns=columns)
    
    df['ZMONEY'] = df['ZMONEY'].apply(pd.to_numeric)

    df.loc[df['DO_TYPE'] == '1', ['ZMONEY']] = df * -1
    df.loc[df['DO_TYPE'] == '3', ['ZMONEY']] = 0
    df.loc[df['DO_TYPE'] == '4', ['ZMONEY']] = 0

    grouped = df.groupby(['WDATE'], as_index = False).agg('sum')

    # grouped = df.groupby(['WDATE'], as_index = False).agg(
    #     lambda x : x.sum() if x.dtype=='float64' else ','.join(x)
    # )
    # print(running_balance.nlargest(5))

    running_balance = grouped['ZMONEY'].cumsum()
    grouped['Running balance'] = running_balance

    return grouped[-50:]

def main():
    raw_data = get_raw_data()
    create_running_balance(raw_data)

if __name__ == "__main__":
    main()
