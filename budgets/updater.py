import pyodbc
import mysql.connector
import time

# Connect to SQL Server
sql_server_conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password')
sql_server_cursor = sql_server_conn.cursor()

# Connect to MySQL
mysql_conn = mysql.connector.connect(host='localhost', database='your_mysql_db', user='your_username',
                                     password='your_password')
mysql_cursor = mysql_conn.cursor()


def sync_data():
    # Query SQL Server for account_ids
    sql_server_cursor.execute('SELECT account_id FROM your_table')
    sql_server_account_ids = [row.account_id for row in sql_server_cursor.fetchall()]

    # Query MySQL for account_ids
    mysql_cursor.execute('SELECT account_id FROM your_table')
    mysql_account_ids = [row[0] for row in mysql_cursor.fetchall()]

    # Find new account_ids in SQL Server and update MySQL
    new_account_ids = set(sql_server_account_ids) - set(mysql_account_ids)

    for account_id in new_account_ids:
        # Retrieve data for the new account_id from SQL Server
        sql_server_cursor.execute('SELECT * FROM your_table WHERE account_id = ?', (account_id,))
        entry = sql_server_cursor.fetchone()

        # Insert data into MySQL for the new account_id
        mysql_cursor.execute('INSERT INTO your_table (column1, column2, account_id) VALUES (%s, %s, %s)',
                             (entry.column1, entry.column2, entry.account_id))

    mysql_conn.commit()


# Run synchronization every hour
while True:
    sync_data()
    time.sleep(3600)  # Sleep for 1 hour before running again