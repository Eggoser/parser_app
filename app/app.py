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

		if counter % 50 == 0:
			update_many(result)
			result = {}

		counter += 1

	return


@app.route("/")
def start_parsing():
	if "parsing_task" in [i.name for i in threading.enumerate()]:
		return "<h1>Скрипт уже был запущен</h1>"


	data = get_all_rows()

	thread = threading.Thread(target=my_background_task, args=(data,))
	thread.name = "parsing_task"
	thread.start()


	return "<h1>Вы запустили скрипт!</h1>"

