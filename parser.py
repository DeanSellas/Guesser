from bs4 import BeautifulSoup
import requests
from contextlib import closing

from fire import Fire

import sys, os


def parse(data, name, outdir="feed"):
    s = ""

    soup = BeautifulSoup(data, 'html.parser')
    
    for p in soup.find_all('p'):
        s += p.get_text()
        s += "\n"
    for p in soup.find_all('span'):
        s += p.get_text()
        s+= "\n"
    for p in soup.find_all('div'):
        s += p.get_text()
        s += "\n"
    
    with open(os.path.join(outdir, "{}.txt".format(name)), 'w', encoding="utf-8") as f:
        f.write(s)


#if __name__ == "__main__":
#    Fire(parse)

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None)

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if(is_good_response(resp)):
                return resp.content

    except:
        return None
        
raw_html = simple_get('https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=10-Q&owner=include&count=40&action=getcurrent')

html = BeautifulSoup(raw_html, 'html.parser')
c = 0
for a in html.select('a'):
    if (a.text == "[text]"):
        print("RUN: {}".format(c))
        data = simple_get("https://www.sec.gov/{}".format(a["href"]))
        parse(data, "test{}".format(c))
    if (c >= 20):
        break
    c += 1