import requests
from bs4 import BeautifulSoup
LIMIT = 50
URL = f"https://ca.indeed.com/jobs?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=Toronto%2C+ON&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"

def get_last_page():
  result = requests.get(URL)
  
  soup = BeautifulSoup(result.text,"html.parser")
  pagination = soup.find("div",{"class": "pagination"})
  
  links = pagination.find_all('a')
  pages = []
  #remove last item in links
  for link in links[:-1]:
    #link.string is possible
    pages.append(int(link.find("span").string))
  
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("h2",{"class":"title"}).find("a")["title"]

  company = html.find("span",{"class": "company"})
  company_anchor = company.find("a")
  if company: 
    if  company_anchor is not None:
      company = str(company.find("a").string)
    else:
      company = str(company.string)
      #strip : delete space 
  else:
    company = None
  company = company.strip()
  #<div id="recJobLoc_b5f2b1af0ddb6dd9" class="recJobLoc" data-rc-loc="Toronto, ON" style="display: none"></div>
  location= html.find("div",{"class": "recJobLoc"})["data-rc-loc"]
  #job_id link - you can apply this posting 
  #<div class="jobsearch-SerpJobCard unifiedRow row result clickcard" id="pj_b5f2b1af0ddb6dd9" data-jk="b5f2b1af0ddb6dd9" data-empn="4436621501141577" data-ci="363091254">
  job_id = html["data-jk"]

  return {'title' : title, 'company': company, 'location': location, "link":f"https://ca.indeed.com/viewjob?jk={job_id}"
  }


def extract_jobs(last_page):
  
  jobs = []
  #whole page print
  for page in range(last_page):
    print (f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    #print(result.status_code)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div",{"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs
