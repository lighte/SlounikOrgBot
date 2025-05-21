import requests
from bs4 import BeautifulSoup, NavigableString, Comment

TELEGRAM_MAX_LENGTH = 4096 # TODO i think this constant is in the Telegram library.

def query_dictionary(term: str) -> str:
	print("start")

	# Replace this with your desired search term
	# search_term = "мова"
	url = f"https://slounik.org/search?dict=&search={term}&un=1"

	print(f"Url is {url}")

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
	#    title = result.find("a").get_text(strip=True)
	#    link = result.find("a")["href"]
	#    print(f"{title}: https://slounik.org{link}")

	print("Results:")
	# print(f"{results[0]}")

	if len(results) == 0:
		return ["Нічога ня знойдзена."] # TODO shoud this avoid getting into cache?

	html_content = str(results[0])

	# Keep only Telegram-supported tags
	allowed_tags = ['b', 'i', 'u', 's', 'a', 'code', 'pre', 'blockquote']

	def clean_for_telegram_html(soup):

	    for element in soup(text=lambda text: isinstance(text, Comment)):
	        element.extract()

	    for tag in soup.find_all(True):
	        if tag.name not in allowed_tags:
	            tag.unwrap()  # remove the tag but keep the content
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