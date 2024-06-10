import requests
from bs4 import BeautifulSoup

# https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term= where <s> is the search term (i.e https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python)


def get_urls(keyword):
    #as of May 26th 2024, this site does not have pagination
    return f'https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}'


def get_jobs_wwr(keyword):
    multiple_urls = get_urls(keyword)
    all_jobs = []

    response = requests.get(
        multiple_urls,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find_all("section", class_="jobs")

    for job in jobs:
        # 회사 이름, 직무 제목, 설명 및 직무 링크
        if job.find("li", class_="feature"):
            continue
        company = job.find("span", class_="company")
        title = job.find("span", class_="title")
        url_of_posting = job.find(
            "div", class_="tooltip--flag-logo").find("a")["href"]

        job_data = {
            "title":
            title.text,
            "company":
            company.text,
            "link":
            f'https://weworkremotely.com/company{url_of_posting}'
        }
        all_jobs.append(job_data)

    return all_jobs
