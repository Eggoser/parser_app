import mysql.connector
from .read_config import read_config


ini_config = read_config()


db = mysql.connector.connect(
  host="localhost",
  user=ini_config["mysql"]["login"],
  password=ini_config["mysql"]["login"],
  database="carlife_2",
  port=3306
)

cursor = db.cursor()


GET_REQUEST = "SELECT id, sku, brand FROM ax_product WHERE gtin is NULL"


def get_all_rows():
	cursor.execute(GET_REQUEST)
	output = cursor.fetchall()

	return output



def update_many(raw):
	for key, value in raw.items():
		cursor.execute("UPDATE ax_product SET gtin={value} WHERE id={key}".format(key=key, value=value))

	db.commit()
