import requests
from bs4 import BeautifulSoup
URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    #<a href="/jobs?q=python&amp;so_source=JobSearch&amp;so_medium=Internal" title="page 1 of 15" class="s-pagination--item is-selected">
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    #print(pages)
    #strip = True : remove whitespace
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    #<h2 class="mb4 fc-black-800 fs-body3">
    #<a href="/jobs/185876/senior-software-engineer-frontend-deepfield-networks?a=10kTLndJTsqc&amp;so=i&amp;pg=2&amp;offset=0&amp;total=361&amp;so_medium=Internal&amp;so_source=JobSearch&amp;q=python" title="Senior Software Engineer (Frontend)" class="s-link stretched-link">Senior Software Engineer (Frontend)</a>
    #</h2>
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    #print(title)
    #<h3 class="fc-black-700 fs-body1 mb4">
    # <span>Deepfield Networks</span>
    # <span class="fc-black-500">Ann Arbor, MI</span>
    #</h3>
    #what is the meaning of recrusive??
    company, location = html.find("h3", {
        "class": "mb4"
    }).find_all(
        "span", recrusive=False)
    print(company.get_text(strip=True), location.get_text(strip=True))

    return {'title': title}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(page + 1)
        result = requests.get(f"{URL}&pg={page+1}")
        #print(result.status_code)
        #<div class="grid--cell fl1 ">
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "grid--cell fl1"})

        for result in results:
            #print(result["data-jobid"])
            job = extract_job(result)
            jobs.append(job)


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
