import requests
from bs4 import BeautifulSoup

def extract_job(html):
    title = html.find("span", {"class": "title"})
    if title:
      title = title.text
    company = html.find("span", {"class": "company"})
    if company:
      company = company.text
    links = html.find_all("a")
    cell_line = []
    for i in links:
        href = i.attrs['href']
        cell_line.append(href)
    a = cell_line[1]
    apply_link = f"https://weworkremotely.com/{a}"


    return{"title":title,"company":company,"apply_link":apply_link}
  
def extract_jobs(url):
    jobs = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("li",{"class":"feature"})
    print("Scrapping WWR-page")
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs

def get_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(url)
  return jobs
