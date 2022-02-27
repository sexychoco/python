import requests
from bs4 import BeautifulSoup


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"}

orginal_url = "https://remoteok.com/"

def extract_job(html):
    item = html.find("td", {"class": "company_and_position"})
    title = item.find("a", {"class": "preventLink"}).find("h2")
    if title:
        title = title.text.strip("\n")
    company = item.find("span", {"class": "companyLink"}).find("h3")
    if company:
        company = company.text.strip("\n")
    link = html.find("td", {"class": "company"}).find("a", {"class": "preventLink"})["href"]
    apply_link = f"{orginal_url}{link}"
    return{"title": title, "company": company, "apply_link": apply_link}

def extract_jobs(url):
    jobs = []
    result = requests.get(url,headers = headers)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("tr", {"class": "job"})
    print("Scrapping ok-page")
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs

def get_jobs(word):
  url = f"https://remoteok.io/remote-{word}-jobs"
  jobs = extract_jobs(url)
  return jobs