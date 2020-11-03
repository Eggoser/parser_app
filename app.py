from database import get_all_rows, update_many
from main import CreateRequest


ROWS_PER_CYCLE = 2


try:
	while True:
		data = get_all_rows(ROWS_PER_CYCLE)

		if not data:
			break

		result = {}

		for pk, query, brand in data:
			gtin = CreateRequest(query, brand).get_ean_number()

			if gtin:
				result[pk] = gtin
			else:
				result[pk] = "0"
		
		update_many(result)



except:
	print("Скрипт завершил выполнение с ошибкой")