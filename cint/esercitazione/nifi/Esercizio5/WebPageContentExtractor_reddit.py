import json
import requests

import urllib
from readability import Document
from bs4 import BeautifulSoup

import os
import fnmatch
import string

import re
from functools import lru_cache
import fileinput





def extractWebPageFromExpandedUrl(url):
    if url is None:
        return None

    if "youtube.com" in url:
        return None
    if "twitter.com" in url:
        return None
    r = requests.get(url)
    if "text/html" in r.headers["content-type"]:
        return extractArticleContent(r.text)
    else:
        return None





def extractWebPageFromShortUrl(urlOriginal):
    url = resolve(urlOriginal)
    return url


def extractArticleContent(content):
    originalHtml = content
    minLength = 1000
    doc = Document(content)
    title = BeautifulSoup(doc.title(), "lxml").text.strip()
    shortTitle = BeautifulSoup(doc.short_title(), "lxml").text.strip()
    cleanContent = BeautifulSoup(doc.summary(), "lxml").text.strip()
    if len(cleanContent) < minLength:
        return None
    return (originalHtml, title, shortTitle, cleanContent)

def extractWebPageArticleContent(url):
    urlExpanded = extractWebPageFromShortUrl(url)
    return extractWebPageFromExpandedUrl(urlExpanded)


def resolve(short_url):
    try:
        session = requests.Session()
        resp = session.head(short_url, allow_redirects=True)
        url = resp.url
        session.close()
        return url
    except:
        return None





# Read data coming from stdin.
line = input()

# Parse JSON data.
parsedJson = json.loads(line)

# Get URL from Reddit submission.
webpage = {}
if "submission" in parsedJson and parsedJson["submission"]["url"] != "":
    url = parsedJson["submission"]["url"]
    content = extractWebPageArticleContent(url)
    if content != None:
        webpage = {"url": url, "title": content[1], "content": content[3]}

parsedJson["webpage"] = webpage
enrichedJson = json.dumps(parsedJson)
print(enrichedJson)




