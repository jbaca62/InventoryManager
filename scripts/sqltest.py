import pyodbc

server = "mysqlserverjbtc.database.windows.net"
database = "TutorialDB"
username = "azureuser"
password = "Jrb@13777"
driver = "{ODBC Driver 17 for SQL Server}"

with pyodbc.connect(
    "DRIVER="
    + driver
    + ";SERVER="
    + server
    + ";PORT=1433;DATABASE="
    + database
    + ";UID="
    + username
    + ";PWD="
    + password
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM dbo.Customers;")
        row = cursor.fetchone()
        while row:
            print(row)
            row = cursor.fetchone()