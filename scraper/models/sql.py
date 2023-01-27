import mysql.connector




mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "scraperdatabase"
   ) 

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE scraperdatabase")
#mycursor.execute("CREATE TABLE varle (title VARCHAR(255),price VARCHAR(255), img VARCHAR(255), link VARCHAR(255), specs VARCHAR(255))")
