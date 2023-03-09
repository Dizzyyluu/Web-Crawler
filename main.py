from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(title, location):
    # generate a url from title and position
    site = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={}&locationstring={}'
    url = site.format(title, location)
    return url

def get_record(card):
    title = card.find('span', class_='noctitle').text.strip()
    location = card.find('li', class_='location').text.strip()
    company = card.find('li', class_='business').text.strip()
    date = card.find('li', class_='date').text.strip()
    salary = card.find('li', class_='salary').text.strip()

    record = (title + "\n\n" + location + "\n\n" + company + "\n\n" + date + "\n\n" + salary)

    return record

def main():
    """Run the main program routine"""
    position = input("Enter job position: ")
    location = input("Enter job location: ")
    records = []

    url = get_url(position, location)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('article', id=lambda x: x and x.startswith('article-'))

    for card in cards:
        record = get_record(card)
        records.append(record)

    for record in records:
        print(record)
        print('\n\n')

if __name__ == '__main__':
    main()
