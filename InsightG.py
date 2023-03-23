import requests
from bs4 import BeautifulSoup

def get_url(page, city, province, country, job_title):
    site = 'https://jobs.insightglobal.com/find_a_job/page/{0}/{1}/?ff=Location,LessThanOrEq,0,0,50&zip={1},{2},{3}&rd=50&miles=False&remote=False&srch={4}&orderby=recent&filterby=&filterbyremote=0'
    url = site.format(page, city.lower(), province, country, job_title.replace(" ", "+"))
    return url

def get_record(result):
    date = result.find('p', class_='date').text.strip()
    job_title = result.find('div', class_='job-title').text.strip()
    job_info = result.find("div", {"class": "job-info"}).find_all("p")
    if len(job_info) >= 2:
        job_location = job_info[0].text.strip()
        job_field = job_info[1].text.strip()
    else:
        job_location = "N/A"
        job_field = "N/A"
    if len(job_info) >= 3:
        job_type = job_info[2].text.strip()
    else:
        job_type = "N/A"

    record = (date + "\n\n" + job_title + "\n\n" + job_location + "\n\n" + job_field + "\n\n" + job_type)

    return record

def main():
    records = []
    
    city = input("Enter the city name: ")
    province= input("Enter the province name: ")
    country = input("Enter the country name: ")
    job_title = input("Enter the job title: ")
    
    url = get_url(1, city, province, country, job_title)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='result')
    
    if not results:
        print("No job postings found.")
    else:
        print(f"Total records found: {len(results)}\n")

        for result in results:
            record = get_record(result)
            print(record + '\n')
            print("---------------------------")
            print('\n')

if __name__ == '__main__':
    main()
