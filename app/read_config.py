import configparser



def read_config():
	config = configparser.ConfigParser()
	config.sections()

	config.read('configuration.ini')


	if "mysql" not in config.sections():
		raise AttributeError("'mysql' parameters are undefined")

	mysql_password = config["mysql"]["password"] if config["mysql"]["password"] != "no" else ""

	result_dict = {}
	result_dict["mysql"] = {"login": config["mysql"]["login"], 
							"password": mysql_password,
							"port": config["mysql"]["port"]}

	return result_dict

