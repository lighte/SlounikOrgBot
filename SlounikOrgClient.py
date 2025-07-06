import requests
from bs4 import BeautifulSoup, NavigableString, Comment
from Logger import get_logger

TELEGRAM_MAX_LENGTH = 4096 # TODO i think this constant is in the Telegram library.
logger = get_logger()

def query_dictionary(term: str) -> str:
	logger.info("start")

	# Replace this with your desired search term
	# search_term = "мова"
	url = f"https://slounik.org/search?dict=&search={term}&un=1"

	logger.info(f"Url is {url}")

	# Send a GET request
	response = requests.get(url)
	response.raise_for_status()  # Raise error if request failed

	# print(f"Response body is {response.text}")

	# Parse the HTML response
	soup = BeautifulSoup(response.text, "html.parser")

	# Example: Find search result entries (you'll need to inspect the real structure)
	results = soup.find_all("ol", class_="results-list")  # Adjust this class based on the site's structure

	# print(f"Results: {results}")

	# Print or process results
	# for result in results:
	#	title = result.find("a").get_text(strip=True)
	#	link = result.find("a")["href"]
	#	print(f"{title}: https://slounik.org{link}")

	#logger.debug("Results size: {results}")
	# print(f"{results[0]}")

	if len(results) == 0:
		logger.debug(f"Nothing found for '{term}'")
		return ["Нічога ня знойдзена."] # TODO shoud this avoid getting into cache?

	html_content = str(results[0])
	logger.debug(f"Length of the response for '{term}' is {len(html_content)}")

	# Keep only Telegram-supported tags
	allowed_tags = ['b', 'i', 'u', 's', 'code', 'pre', 'blockquote'] # Removed `a`.

	def clean_for_telegram_html(soup):

		for element in soup(text=lambda text: isinstance(text, Comment)):
			element.extract()

		# Apply special logic to <a class="my-value"> tags
		for a_tag in soup.find_all('a', class_='results-list-number'):
			# u_tag = soup.new_tag('u')
			bold_tag = soup.new_tag('b')
			bold_tag.string = '('+ a_tag.get_text(strip=True) + ') '
			# bold_tag.insert(0, u_tag)
			a_tag.next_sibling.next_sibling.contents[0].replace_with(bold_tag)#insert(0, bold_tag)# replacc_with(bold_tag)


			# if isinstance(a_tag.next_sibling, NavigableString) and len(a_tag.next_sibling.get_text()) == 0:
				# logger.debug('decomposing empty string element')
			a_tag.next_sibling.decompose()
			a_tag.decompose()
			# a_tag.replace_with(bold_tag)

			# Replace any newline characters immediately after the bold tag with ". "
			# next_elem = a_tag.next_sibling
			# if isinstance(next_elem, str):
			# 	logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> next instance')
			# 	logger.info(f">>>> next_elem.lstrip(): '{len(next_elem.lstrip())}'")
			# 	a_tag.insert_after(next_elem.lstrip().replace('\n', '. ', 1))
			# next_elem = next_elem.next_sibling
			# if isinstance(next_elem, str):
			# 	logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> next instance')
			# 	logger.info(f">>>> next_elem.lstrip(): '{len(next_elem.lstrip())}'")
			# 	a_tag.insert_after(next_elem.lstrip().replace('\n', '. ', 1))
			# next_elem = next_elem.next_sibling
			# if isinstance(next_elem, str):
			# 	logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> next instance')
			# 	logger.info(f">>>> next_elem.lstrip(): '{len(next_elem.lstrip())}'")
			# 	a_tag.insert_after(next_elem.lstrip().replace('\n', '. ', 1))
			# next_elem = next_elem.next_sibling
			# if isinstance(next_elem, str):
			# 	logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> next instance')
			# 	logger.info(f">>>> next_elem.lstrip(): '{len(next_elem.lstrip())}'")
			# 	a_tag.insert_after(next_elem.lstrip().replace('\n', '. ', 1))
			# next_elem = next_elem.next_sibling
			# if isinstance(next_elem, str):
			# 	logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> next instance')
			# 	logger.info(f">>>> next_elem.lstrip(): '{len(next_elem.lstrip())}'")
			# 	a_tag.insert_after(next_elem.lstrip().replace('\n', '. ', 1))

		for tag in list(soup.find_all(True)):
			if tag.name not in allowed_tags:
				# if tag.name == 'a':
				# 	link_text = tag.get_text(strip=True)
				# 	bold_node = NavigableString(f"*{link_text}. *")

				# 	# Insert the bold text before the <a> tag
				# 	tag.insert_before(bold_node)

				# 	# Remove the <a> tag
				# 	tag.decompose()
				# 	logger.info("Removed an `a` tag.")
				# elif tag.parent:  # Check tag is still in the tree
					# logger.info(str(tag))
					# try:
					#	 logger.info(str(tag))
					# except Exception as e:
					#	 logger.warning(f"Could not stringify tag: {repr(tag)} – {e}")
				tag.unwrap()  # remove the tag but keep the content

		logger.debug(str(soup))
		return str(soup)


	def split_text(text: str, max_length: int = TELEGRAM_MAX_LENGTH) -> list[str]:
		# print(text)
		paragraphs = text.split("\n")
		chunks = []
		current_chunk = ""

		for para in paragraphs:
			# print(f"para ---------------------------------------------------{para}")
			if len(current_chunk) + len(para) + 1 <= max_length:
				current_chunk += para + "\n"
			else:
				chunks.append(current_chunk.strip())
				current_chunk = para + "\n"

		if current_chunk:
			chunks.append(current_chunk.strip())

		return chunks

	clean_html = clean_for_telegram_html(BeautifulSoup(html_content, "html.parser"))
	# print(clean_html)

	return split_text(clean_html)