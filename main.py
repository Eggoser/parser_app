import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint


regex_template_for_ean = re.compile(r"[0-9]{13}")

first = re.compile(r"\/ru\/part\/[A-Za-z0-9\-\_]+\/\w+\/")
second = re.compile(r"\/ru\/search\/product\/[A-Za-z0-9\-\_]+\/\w+\/")



class ParseException(Exception):
	pass


class CreateRequest:
	def __init__(self, query, brand=None):
		template = "https://renix.com.ua/ru/search/?query={}"

		self.url = template.format(query)
		self.brand = brand


	def make_request(self):
		self.response = requests.get(self.url)
		self.data = self.response.text

		self.soup = BeautifulSoup(self.data, "html.parser")

	def clean_varriables(self):
		del self.data, self.response, self.soup


	def start_parsing(self):
		self.make_request()


		# parsing body
		# many_flag = False
		# table = self.soup.find("table")

		# rows = [i for i in table.findAll("tr") if " ".join(i["class"]) != "brand-article"]


		# if len(rows) > 1:
		# 	if not self.brand:
		# 		raise ParseException("brand not set")

		# 	many_flag = True

		# 	for i in rows:
		# 		local_brand = i.find("td", {"class": "data-cell align-middle"}).find("div").text

		# 		if local_brand.lower() == self.brand.lower():
		# 			row = i
		# 			break

		# else:
		# 	row = rows[0]


		# if not many_flag:
		# 	name_with_url = row.findAll("td")[1].find("a")

		# else:
		# 	name_with_url = row.findAll("td")[-1].find("a")

		# url_prefix = name_with_url["href"]

		# if many_flag:
		# 	url_prefix = url_prefix.replace("/search/product", "/part")
		
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
		try:
			self.start_parsing()
		except:
			return None

		self.make_request()


		# parsing body
		try:
			parameter_place = self.soup.find("div", {"class": "col-lg-6 table-responsive"})
			table = parameter_place.find("table")

			rows = table.findAll("tr")
		except: return None

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
