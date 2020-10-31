from flask import Flask
from celery import Celery
import itertools

from .database import get_all_rows, update_many
from .main import CreateRequest

CELERY_THREADS = 100


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def my_background_task(big_array):
	result = {}
	print("task has been started")

	for pk, query, brand in big_array:
		gtin = CreateRequest(query, brand).get_ean_number()
		if gtin:
			result[pk] = gtin
	print(len(result))


	update_many(result)

	return

@celery.task
def print_govno():
	print("govnooooo")


@celery.task
def update_file():
        with open("app/flag_starts_file", "w") as fw:
                        fw.write("0")


@app.route("/")
def start_parsing():
	with open("app/flag_starts_file") as f:
		content = f.read()

		if content == "1":
			return "<h1>Скрипт уже был запущен</h1>"

		with open("app/flag_starts_file", "w") as fw:
			fw.write("1")


	data = get_all_rows()
	print(len(data))


	step = len(data) // (CELERY_THREADS - 1)
	# for i in range(0, len(data), tasks_for_one_thread):
	# 	# print(len(data[i:i+tasks_for_one_thread]))
	# 	my_background_task.delay(data[i:i+tasks_for_one_thread])

	# # print(len(list(itertools.islice(reversed(data), len(data)%CELERY_THREADS))))
	# my_background_task.delay(list(itertools.islice(reversed(data), len(data)%CELERY_THREADS)))

	all_tasks = len(data)
	start = 0

	while all_tasks - step > 0:
		my_background_task(data[start:start+step])

		start += step
		all_tasks -= step

	my_background_task.delay(list(itertools.islice(reversed(data), all_tasks)))

	update_file.delay()



	return "<h1>Вы запустили скрипт!</h1>"



if __name__ == "__main__":
	app.run()