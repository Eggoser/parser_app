import mysql.connector
from read_config import read_config


ini_config = read_config()





GET_REQUEST = "SELECT id, sku, brand FROM ax_product WHERE gtin is NULL limit {}"


def get_all_rows(count_rows):
	db = mysql.connector.connect(
	  host="localhost",
	  user=ini_config["mysql"]["login"],
	  password=ini_config["mysql"]["password"],
	  database=ini_config["mysql"]["database"],
	)

	cursor = db.cursor()

	cursor.execute(GET_REQUEST.format(str(count_rows)))
	output = cursor.fetchall()

	cursor.close()
	db.close()

	return output



def update_many(raw):
	db = mysql.connector.connect(
	  host="localhost",
	  user=ini_config["mysql"]["login"],
	  password=ini_config["mysql"]["password"],
	  database=ini_config["mysql"]["database"],
	)

	cursor = db.cursor()

	for key, value in raw.items():
		cursor.execute("UPDATE ax_product SET gtin={value} WHERE id={key}".format(key=key, value=value))

	db.commit()

	cursor.close()
	db.close()
