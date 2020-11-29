import configparser
import os

filename = os.path.join(os.path.dirname(__file__), "configuration.ini")


def read_config():
	config = configparser.ConfigParser()
	config.sections()

	config.read(filename)


	if "mysql" not in config.sections():
		raise AttributeError("'mysql' parameters are undefined")

	mysql_password = config["mysql"]["password"] if config["mysql"]["password"] != "no" else ""

	result_dict = {}
	result_dict["mysql"] = {"login": config["mysql"]["login"], 
							"password": mysql_password,
							"database": config["mysql"]["database"]}

	return result_dict

