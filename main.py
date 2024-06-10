from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from extractor.berlinstartup import get_jobs_ber
from extractor.web3 import get_jobs_web3
from extractor.weworkremotely import get_jobs_wwr

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs = db[keyword]
    else:
        berstartup = get_jobs_ber(keyword)
        wwr = get_jobs_wwr(keyword)
        web3 = get_jobs_web3(keyword)
        jobs = berstartup + wwr + web3
        db[keyword] = jobs

    return render_template("search.html", keyword=keyword, jobs=jobs)


app.run("0.0.0.0")
