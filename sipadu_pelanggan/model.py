import mysql.connector
import sys

def query(query,data=None):
	try:
		db = mysql.connector.connect(user="root",password="jaki",database="sipadu")
		c = db.cursor()
		c.execute(query,data)
		db.commit()
		return c.lastrowid
	except mysql.connector.errors.ProgrammingError as e:
		print e
		raise
	finally:
		db.close()
		c.close()

def get_query(query,data=None):
	try:
		db = mysql.connector.connect(user="root",password="jaki",database="sipadu")
		c = db.cursor()
		c.execute(query,data)
		res = c.fetchall()
		
		if(len(res)==0): return None
		
		col_names = c.column_names
		result = []
		for r in res:
			row = {}
			for i in range(len(r)):
				col = str(r[i])		
				row[col_names[i]] = col
			result.append(row)
		return result
	except mysql.connector.errors.ProgrammingError as e:
		print e
		raise
	finally:
		db.close()
		c.close()
		
