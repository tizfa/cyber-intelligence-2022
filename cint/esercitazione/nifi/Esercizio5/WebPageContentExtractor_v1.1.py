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



"""
The regex patterns in this gist are intended only to match web URLs -- http,
https, and naked domains like "example.com". For a pattern that attempts to
match all URLs, regardless of protocol, see: https://gist.github.com/gruber/249502
"""
WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""



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

def extractUrls(text):
    return re.findall(WEB_URL_REGEX, text)




# Read data coming from stdin.
line = input()

# Parse JSON data.
parsedJson = json.loads(line)

# Get tweet text.
text = parsedJson["text"]
if "extended_tweet" in parsedJson:
   text = parsedJson["extended_tweet"]["full_text"]


# Extract all urls from tweet.
urls = extractUrls(text)

webpage = {}
for url in urls:
    content = extractWebPageArticleContent(url)
    if content is None:
        continue
    webpage = {"url": url,"title":content[1],"content":content[3]}
    break 

parsedJson["webpage"] = webpage
enrichedJson = json.dumps(parsedJson)
print(enrichedJson)




