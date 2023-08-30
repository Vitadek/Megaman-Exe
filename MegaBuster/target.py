#!/usr/bin/python3
class Target:
	
	def __init__(self, name, ip):
		"Creates a target upon class call"
		self.name = name
		self.ip = ip
		self.info = {
		"name": self.name,
		"ip" : self.ip		
		}

	def get_name(self):
		return self.name

	def get_ip(self):
		return self.ip

	def get_info(self) -> dict:
		return self.info
	
	def delete_element(self, element):
		self.info.pop(element)
	
	def append_element(self, element, value):
		self.info[element] = value
	
	def set_info_element(self, element, value):
		self.info.update({element: value})
		

	def test_print(self):
		print(self.info)

	

