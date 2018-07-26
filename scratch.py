import requests
from bs4 import BeautifulSoup



fact="the quick brown fox jumps of the lazy dog"
response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/",
                         data={'input_text': f"{fact}"}, allow_redirects=False)
loc = response.headers.get("Location")
result = requests.get(loc)

soup = BeautifulSoup(result.content, "html.parser")
pig = soup.find("body").getText().split('\t')[1].strip()

x=1