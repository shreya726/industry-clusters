from bs4 import BeautifulSoup
import sys
import time
import os
import requests
import codecs
import json
import unicodecsv as csv
import random
import urllib.request
from html2text import html2text
from pathlib import Path

base_url = "http://www.indeed.com"

def parse_joblist_page(joblist_page_url,filename):
    # Sleep before starting a new http request
    seconds = (random.random() * 2) + (random.random() * 5)
    time.sleep(seconds)

    response = urllib.request.urlopen(joblist_page_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract urls to specific jobs
    job_boxes = soup.select("div.row.result")
    for job_box in job_boxes:
        if len(job_box.select("span.sdn")) > 0:
            continue
        if len(job_box.select("div.iaP")) > 0:
            job_url = job_box.findAll("a", {"data-tn-element": "jobTitle"})[0]["href"]
            if job_url.startswith("/rc/clk"):
                job_url = job_url.replace('/rc/clk', '/viewjob', 1)
            if job_url.startswith("/company"):
                job_url = job_url.replace('/company', '/cmp', 1)
            if job_url.startswith("/cmp") or job_url.startswith("/viewjob"):
                parse_job_page(job_url,filename)

    # Get next URL page if exists
    try:
    	nav_items = soup.select("div.pagination")[0].select("a")
    	for nav_item in nav_items:
    		for button in nav_item.select("span.np"):
    			if "Next" in button.text:
    				return(base_url + nav_item["href"],True)
    except:
    	pass
    return (None, False)

def parse_job_page(job_page_url,filename):
    if job_page_url in saved:
        return
    else:
        saved.append(job_page_url)
    url = base_url + job_page_url

    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract needed information
    job_title = soup.select("b.jobtitle")[0].text
    company = soup.select("span.company")[0].text
    location = soup.select("span.location")[0].text
    job_description = html2text(soup.find("span", {"id" : "job_summary"}).text)
    with open(filename, 'ab') as fout:
        writer = csv.DictWriter(fout, fieldnames = ['job_title', 'job_description', 'location', 'company'], delimiter = ',')
        data = {'job_title':job_title, 'job_description':job_description, 'location':location, 'company':company}
        writer.writerow(data)


with open('top_cities.csv','r') as src:
    i = 0
    for line in src:
        i+=1
        # to get remaining datasets.
        if i < 26 or i > 32: continue
        line = line.split(',')
        # Skips header.
        if line[0] == "job_category": continue
        # Job category
        job_category = line[0].split('/')
        if len(job_category) > 1:
            job_category = '%2C'.join(job_category)
        else:
            job_category = job_category[0]
            job_category = job_category.replace(' ','+')

        
        # Top 10 cities, per CSV.
        for i in range(1,11):
            city = line[i*2 -1].replace(' ','+').replace('"','')
            state = line[i*2].replace('"','').replace(' ','')
            location = '%2C'.join([city,state])
            # URL based on job category and location.
            url = base_url + "/jobs?q=" + job_category + "&l=" + location
            # CSV results filename based on job category and city.
            filename = "dataset/"+job_category.replace('+','_').replace('%2C','_') + city.replace('+','') + '.csv'
            if Path(filename).is_file():
                continue
            else:
                with open(filename, 'wb') as fout:
                    writer = csv.DictWriter(fout, fieldnames = ['job_title', 'job_description', 'location', 'company'], delimiter = ',')
                    writer.writeheader()
                notFinished = True
                saved = []
                while(notFinished):
                    (url, notFinished) = parse_joblist_page(url, filename)
    print('Finished parsing all cities.')
#eof
