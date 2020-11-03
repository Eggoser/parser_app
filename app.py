from .database import get_all_rows, update_many
from .main import CreateRequest


ROWS_PER_CYCLE = 50


def my_background_task(big_array):
	result = {}
	l = len(big_array)


	counter = 0
	

		if counter % 50 == 0:
			

		counter += 1

	return


try:
	while True:
		data = get_all_rows(ROWS_PER_CYCLE)

		if not data:
			break

		for pk, query, brand in big_array:
			gtin = CreateRequest(query, brand).get_ean_number()

			if gtin:
				result[pk] = gtin
			else:
				result[pk] = "0"

		for i, k in data.items():
			print("id: {} | gtin: {}".format(i, k))
			update_many(result)
			result = {}



except:
	print("Скрипт завершил выполнение с ошибкой")