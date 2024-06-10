import requests
from bs4 import BeautifulSoup


def get_urls(keyword):
    #as of May 26th 2024, this site does not have pagination
    return f'https://berlinstartupjobs.com/skill-areas/{keyword}/'


def get_jobs_ber(keyword):
    all_jobs = []

    page = get_urls(keyword)

    response = requests.get(
        page,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("ul",
                     class_="jobs-list-items").find_all("li",
                                                        class_="bjs-jlid")
    for job in jobs:
        # 회사 이름, 직무 제목, 설명 및 직무 링크
        if job.find("a", class_="bjs-jlid__b") is None:
            continue
        company = job.find("a", class_="bjs-jlid__b")
        title = job.find("h4", class_="bjs-jlid__h")
        description = job.find("div", class_="bjs-jlid__description")
        url_of_posting = job.find("h4", class_="bjs-jlid__h").find("a")["href"]

        job_data = {
            "title": title.text,
            "company": company.text,
            "Description": description.text,
            "link": url_of_posting
        }
        all_jobs.append(job_data)

    return all_jobs
