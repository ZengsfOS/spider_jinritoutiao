import requests
from urllib.parse import urlencode
import traceback
import os
from hashlib import md5


base_url = "https://www.toutiao.com/search_content/?"


amount_size = 20

def get_page(offset):
	params = {
		'offset' : offset,
		'format' : 'json',
		'keyword' : '街拍',
		'autoload' : 'true',
		'count' : '20',
		'cur_tab' : '1',
		'from' : 'search_tab',
		}	
	url = base_url + urlencode(params)
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.json()
	except requests.ConnectionError as e:
		traceback.print_exc()
		return

def get_images(json):
	if json.get("data"):
		for item in json.get("data"):
			if item.get("cell_type") is not None:
				continue
			title = item.get("title")
			images = item.get("image_list")
			try:
				for image in images:
					yield{
						"image":image.get("url"),
						"title":title
				 	}
			except TypeError:
				continue

def save_image(item):
	if not os.path.exists(item.get("title")):
		os.mkdir(item.get("title"))
	try:
	#这里要加一个http:要不然会报错requests.exceptions.MissingSchema: Invalid URL 'xxxxxxxxxxxxx': No schema supplied. Perhaps you meant xxxxxxxxxxxxx
		response = requests.get("http:" + item.get("image"))
		if response.status_code == 200:
			file_path = "{0}/{1}.{2}".format(item.get("title"), md5(response.content).hexdigest(), "jpg")
			if not os.path.exists(file_path):
				with open(file_path, "wb") as f:
					f.write(response.content)
			else:
				print("Already Downloaded", file_path)
	except requests.ConnectionError as e:
		tracebace.print_exc()


def main():
	for page in range(1, amount_size):
		json = get_page(page)
		for item in get_images(json):
			print(item)
			save_image(item)
		
	

if __name__ == "__main__":
	main()

