import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find("div", {"class":"pagination"}).find_all("a")
  last_pages = pages[-2].get_text(strip=True)
  return int(last_pages)

def extract_job(html):
  title = html.find("h2", {"class":"job_tit"}).find("a")["title"]
  company = html.find("strong", {"class":"corp_name"}).find("a")["title"]
  job_condition = html.find("div", {"class":"job_condition"}).get_text()
  job_id = html["value"]
  return {
    'title':title,
    'company':company,
    'job_condition':job_condition,
    'apply_link':f"https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}"
  }

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SR: Page: {page}")
    result = requests.get(f"{url}&recruitPage={page+1}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class":"item_recruit"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
  return jobs



def get_jobs(word):
  url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={word}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs