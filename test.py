import requests

url = "https://www.globalfirepower.com/aircraft-total.php"

response = requests.get(url)

print(response.text)
import requests
from bs4 import BeautifulSoup

url = "https://www.globalfirepower.com/aircraft-total.php"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.prettify())
