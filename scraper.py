import requests
from bs4 import BeautifulSoup
import time
import random

reviews_txt_list = []

for i in range(1,19):
    time.sleep(random.uniform(1,3))

    url = f"https://www.drugs.com/comments/fluoxetine/prozac-for-depression.html?page={i}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    session = requests.Session() 
    session.headers.update(headers)
    response = session.get(url)
    print(response.status_code)
    source = response.text
    soup = BeautifulSoup(source, 'html.parser')

    review_text = soup.find_all("div", {"class": "ddc-comment ddc-box ddc-mgb-2"})

    for review in review_text:
        review = BeautifulSoup(str(review), 'html.parser')
        review_txt_content = review.p.text
        reviews_txt_list.append(review_txt_content)
    print(len(reviews_txt_list))

print(len(reviews_txt_list))