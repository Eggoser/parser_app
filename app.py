from database import get_all_rows, update_many
from main import CreateRequest
from requests.exceptions import ReadTimeout
from mysql.connector.errors import DatabaseError
from exceptions import OtherError



ROWS_PER_CYCLE = 2


try:
	while True:
		data = get_all_rows(ROWS_PER_CYCLE)

		if not data:
			break

		result = {}

		for pk, query, brand in data:
			try:
				gtin = CreateRequest(query, brand).get_ean_number()
			except KeyboardInterrupt:
				raise KeyboardInterrupt
			except OtherError as err:
				with open("file.log", "a") as log:
					log.write(str(err))
			except:
				gtin = None

			if gtin:
				result[pk] = gtin
				print("[+] sku: {} brand: {} gtin: {}".format(pk, brand, gtin))
			else:
				result[pk] = "0"
				print("[-] sku: {} brand: {}".format(pk, brand))

		try:
			update_many(result)
		except DatabaseError:
			pass


except:
	print("Script has been ending with error")
