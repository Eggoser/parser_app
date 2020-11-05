import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint


regex_template_for_ean = re.compile(r"[0-9]{13}")

first = re.compile(r"\/ru\/part\/[A-Za-z0-9\-\_]+\/\w+\/")
second = re.compile(r"\/ru\/search\/product\/[A-Za-z0-9\-\_]+\/\w+\/")


PROXY = "https://VZG5oC:6mAbTJ@104.227.86.215:8000"


class ParseException(Exception):
	pass


class CreateRequest:
	def __init__(self, query, brand=None):
		template = "https://renix.com.ua/ru/search/?query={}"

		self.url = template.format(query)
		self.brand = brand


	def make_request(self):
		self.response = requests.get(self.url, proxies={"https": PROXY})
		self.data = self.response.text

		self.soup = BeautifulSoup(self.data, "html.parser")

	def clean_varriables(self):
		del self.data, self.response, self.soup


	def start_parsing(self):
		self.make_request()


		p1 = first.findall(self.data)
		if not p1:
			p2 = second.findall(self.data)
			for i in p2:
				test_brand, test_id = re.findall(r"\/ru\/search\/product\/([A-Za-z0-9\-\_]+)\/(\w+)", i)[0]

				if test_brand.lower() == self.brand.lower():
					url_prefix = "/ru/part/" + test_brand + "/" + test_id
					break

		else:
			url_prefix = p1[0]



		# finally
		parsed_url = "https://renix.com.ua" + url_prefix
		self.clean_varriables()
		self.url = str(parsed_url)


	def get_ean_number(self):
		self.start_parsing()


		self.make_request()


		# parsing body
		parameter_place = self.soup.find("div", {"class": "col-lg-6 table-responsive"})
		table = parameter_place.find("table")

		rows = table.findAll("tr")

		results = []

		for i in rows:
			key, value = i.findAll("td")
			key, value = key.text, value.text


			if regex_template_for_ean.fullmatch(value):
				results.append([key.lower(), value])

		if len(results) > 1:
			for i, k in results:
				if "ean" in i or "gtin" in i:
					return k
			return [0][1]

		elif len(results) == 1:
			return results[0][1]
		return None
