import requests
from bs4 import BeautifulSoup

# https://web3.career/-jobs where <s> is the search term (i.e https://web3.career/python-jobs)


def get_urls(skill):
    # for pagination, here we count the number of pages and return the urls

    multiple_urls = []
    page = 1

    while True:
        url = f'https://web3.career/{skill}-jobs?page={page}'

        response = requests.get(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                'Accept-Language': 'en-US,en;q=0.5'
            })

        # if response.status_code != 200:
        #     print("Oops something is wrong here")
        #     break

        # else:
        soup = BeautifulSoup(response.content, "html.parser")

        # count the number of pages until next button is deactivated
        if soup.find("li", class_="page-item next"):
            multiple_urls.append(url)
            page += 1
        else:
            page += 1
            multiple_urls.append(url)
            break
    return multiple_urls


def get_jobs_web3(keyword):
    all_jobs = []

    all_urls = get_urls(keyword)

    for page in all_urls:
        response = requests.get(
            page,
            headers={
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            })
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find("tbody", class_='tbody').find_all("tr", class_="table_row")

        for job in jobs:
            # 회사 이름, 직무 제목, 설명 및 직무 링크
            if job.find("h3") is None:
                continue
            company = job.find("h3").text
            title = job.find("h2",
                             class_="fs-6 fs-md-5 fw-bold my-primary").text
            url_of_posting = job.find("a")["href"]

            job_data = {
                "title": title,
                "company": company,
                # "Description": description.text,
                "link": f'https://web3.career{url_of_posting}'
            }

            all_jobs.append(job_data)
    return all_jobs
