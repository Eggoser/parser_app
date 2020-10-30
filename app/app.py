from flask import Flask
from celery import Celery
import itertools

from database import get_all_rows, update_many
from main import CreateRequest

CELERY_THREADS = 100


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


celery = Celery("parser_app", broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def my_background_task(big_array):
	result = {}

	for pk, query, brand in big_array:
		gtin = CreateRequest(query, brand).get_ean_number()
		if gtin:
			result[pk] = gtin


	update_many(result)

	return


@app.route("/")
def start_parsing():
	with open("flag_starts_file") as f:
		content = f.read()

		if content == "1":
			return "<h1>Скрипт уже был запущен</h1>"

		with open("flag_starts_file", "w") as fw:
			fw.write("0")


	data = get_all_rows()


	tasks_for_one_thread = len(data) // CELERY_THREADS
	for i in range(0, len(data), tasks_for_one_thread - 1):
		my_background_task.delay(data[i:tasks_for_one_thread])

	my_background_task.delay(list(itertools.islice(reversed(data), len(data)%CELERY_THREADS)))



	return "<h1>Вы запустили скрипт!</h1>"



if __name__ == "__main__":
	app.run()