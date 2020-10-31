from flask import Flask
import threading
import itertools

from .database import get_all_rows, update_many
from .main import CreateRequest


app = Flask(__name__)


def my_background_task(big_array):
	result = {}
	l = len(big_array)


	counter = 0
	for pk, query, brand in big_array:
		gtin = CreateRequest(query, brand).get_ean_number()

		if gtin:
			result[pk] = gtin

		print(pk, query, brand, gtin, "{}/{}".format(big_array, counter))
		counter += 1

	update_many(result)

	with open("app/flag_starts_file", "w") as f:
		content = f.write("0")

	return


@app.route("/")
def start_parsing():
	with open("app/flag_starts_file") as f:
		content = f.read()

		if content == "1":
			return "<h1>Скрипт уже был запущен</h1>"

		with open("app/flag_starts_file", "w") as fw:
			fw.write("1")


	data = get_all_rows()

	thread = threading.Thread(target=my_background_task, args=(data,))
	thread.start()


	return "<h1>Вы запустили скрипт!</h1>"

