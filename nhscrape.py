from bs4 import BeautifulSoup
import requests
import json
import re

class FrontPage:
	@staticmethod
	def get():
		url_home = 'https://nhentai.net'
		response = requests.get(url_home, timeout=5)
		content = BeautifulSoup(response.content, "html.parser")

		bookArr = []
		for book in content.findAll('div', attrs={"class": "gallery"}):
			title = book.find('div', attrs={"class": "caption"}).text
			url_path = book.find('a', attrs={"class": "cover"})['href']
			try:
				image_url = '{}cover.jpg'.format(book.find('img')['data-src'][:-9])
			except KeyError:
				# Some books do not have a 'data-src' URL and throw a KeyError
				# This grabs the thumbnail image in a different attribute
				image_url = 'http:{}cover.jpg'.format(book.find('img')['src'][:-9])
			bookObject = {
				"title": title,
				"url": f'{url_home}{url_path}',
				"image_url": image_url
			}
			bookArr.append(bookObject)
		return bookArr

class SearchResults:
	@staticmethod
	def get(query, page=1, popular=False):
		query = query.split()
		query = '+'.join(query)
		url_home = 'https://nhentai.net'

		if (popular):
			url = f'https://nhentai.net/search/?q={query}&page={page}&sort=popular'
		else:
			url = f'https://nhentai.net/search/?q={query}&page={page}'
		response = requests.get(url, timeout=5)
		content = BeautifulSoup(response.content, "html.parser")

		bookArr = []
		for book in content.findAll('div', attrs={"class": "gallery"}):
			title = book.find('div', attrs={"class": "caption"}).text
			url_path = book.find('a', attrs={"class": "cover"})['href']
			try:
				image_url = '{}cover.jpg'.format(book.find('img')['data-src'][:-9])
			except KeyError:
				# Some books do not have a 'data-src' URL and throw a KeyError
				# This grabs the thumbnail image in a different attribute
				image_url = 'http:{}cover.jpg'.format(book.find('img')['src'][:-9])
			bookObject = {
				"title": title,
				"url": f'{url_home}{url_path}',
				"image_url": image_url
			}
			bookArr.append(bookObject)
		return bookArr

class BookResults:
	@staticmethod
	def _parse_input_(input):
		url_exp = re.compile(r'(http(s)?:\/\/.)?(www\.)?[nhentai]{2,256}\.[net]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
		id_exp = re.compile(r'\d{5,9}')

		if (url_exp.match(input)):
			return input
		elif (id_exp.match(input)):
			return f'https://nhentai.net/g/{input}'
		else:
			raise SyntaxError()

	@staticmethod
	def _parse_image_(image):
		image = image[:8] + 'i' + image[9:]
		image = image[:-5]
		image = image + '.jpg'
		return image
		

	@staticmethod
	def get(id):
		try:
			url = BookResults._parse_input_(id)
			response = requests.get(url, timeout=5)
			content = BeautifulSoup(response.content, "html.parser")

			bookArr = []
			for book in content.findAll('div', attrs={"class": "thumb-container"}):
				try:
					image_thumb = book.find('img')['data-src']
					image_full = BookResults._parse_image_(image_thumb)
				except KeyError:
					image_thumb = book.find('img')['src']
					image_full = BookResults._parse_image_(image_thumb)
				
				bookObject = {
					"thumbnail": image_thumb,
					"full_res": image_full
				}
				bookArr.append(bookObject)
			return bookArr
		except SyntaxError:
			return print('Usage: get(123456) OR get(http://nhentai.net/g/123456)')

	@staticmethod
	def getInfoFromBook(id):
		try:
			url = BookResults._parse_input_(id)
			response = requests.get(url, timeout=5)
			content = BeautifulSoup(response.content, "html.parser")

			contArr = []
			titleObject = {
				"title": content.find('meta', attrs={"itemprop": "name"})['content']
			}

			contArr.append(titleObject)

			try:
				coverEl = content.find('div', attrs={"id": "cover"})
				cover_image = coverEl.find('img')['data-src']
			except KeyError:
				cover_image = coverEl.find('img')['src']

			contArr.append({"cover": cover_image})

			tag_string = content.find('meta', attrs={"name": "twitter:description"})['content']
			tag_string = tag_string.replace(', ', ' ')
			tag_list = tag_string.split()

			tagObject = {
				"tags": tag_list
			}
			
			contArr.append(tagObject)

			return contArr

		except SyntaxError:
			return print('Usage: get(123456) OR get(http://nhentai.net/g/123456)')