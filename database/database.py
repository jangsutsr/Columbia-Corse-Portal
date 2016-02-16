import psycopg2

conn = psycopg2.connect(database='', user='st2957', password='MWRSCW', host='w4111db.eastus.cloudapp.azure.com')
cur = conn.cursor()

conn.commit()
conn.close()
