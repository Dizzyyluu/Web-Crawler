import requests
from bs4 import BeautifulSoup

def get_url(title, location, page):
    site = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?page={}&searchstring={}&locationstring={}'
    url = site.format(page, title, location)
    return url

def get_record(card):
    title = card.find('span', class_='noctitle').text.strip()
    location = card.find('li', class_='location').text.strip().replace('\n', '')
    company = card.find('li', class_='business').text.strip().replace('\n', '')
    date = card.find('li', class_='date').text.strip()
    try:
        salary = card.find('li', class_='salary').text.strip().replace('\n', '')
    except AttributeError:
        salary = 'Unavailable'
    
    record = f"{title}\n{location}\n\n{company}\n\n{date}\n\n{salary}\n"
    
    return record

def scrape_all_results(title, location):
    records = []
    
    page = 1
    while True:
        url = get_url(title, location, page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('article', id=lambda x: x and x.startswith('article-'))
        
        if not cards:
            break
            
        for card in cards:
            record = get_record(card)
            records.append(record)
            
        page += 1
    
    return records

if __name__ == '__main__':
    position = input("Enter job position: ")
    location = input("Enter job location: ")
    
    records = scrape_all_results(position, location)
    print('\n')
    print(f"Total records found: {len(records)}" + '\n')
    
    for record in records:
        print(record + '\n')
