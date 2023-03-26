import requests
from bs4 import BeautifulSoup


def get_url(location, job_title):
    website = f"https://www.kijiji.ca/b-jobs/{location}/{job_title}/k0c45l1700273"
    url = website.format(location, job_title)
    return url


def get_record(card):
    title = card.find('a', class_='title').text.strip()
    description = card.find('td', class_='description').text.strip()
    date = card.find('td', class_='posted').text.strip()
    "\033[1m" + title + "\033[0m"

    record =(("\033[1m" + title + "\033[0m") + "\n\n" + " ".join(description.split()) + "\n\n" + date)
    return record


def main():
    location = input('Enter job location: ')
    position = input('Enter job position: ')
    url = get_url(location, position)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('table', class_='regular-ad')

    if not cards:
        print('No job listings found.')
        return

    for card in cards:
        record = get_record(card)
        total = len(cards)
        print(total)
        print(record)
        print("-------------------")

if __name__ == '__main__':
    main()
