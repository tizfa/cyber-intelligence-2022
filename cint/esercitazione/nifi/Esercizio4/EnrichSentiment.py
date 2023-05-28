import fileinput
import json

from bs4 import BeautifulSoup
from polyglot.text import Text

import re

# Remove any URL from text.
def removeURLs(text):
    cleanText = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    return cleanText

# Remove all special chars from text.
def removeSpecialChars(text):
    cleanText = re.sub(r'[\r\n]+', ' ', text, flags=re.MULTILINE)
    return cleanText


# Get a clean tweet text.
def cleanTweetText(text, toLower= False, mustRemoveURLs=False):
    if toLower:
        textRet = text.lower()
    else:
        textRet = text
    if mustRemoveURLs:
        textRet = removeURLs(textRet)
    textRet = removeSpecialChars(textRet)
    return textRet


def getSentimentPolarity(text):
    # Prepare tweet text to be analyzed with polyglot.
    textForAnalysis = Text(text, hint_language_code="en")
    tweetPolarity = 0
    for w in textForAnalysis.words:
        tweetPolarity = tweetPolarity + w.polarity

    return tweetPolarity





# Read data coming from stdin. 
line = input()

# Parse JSON data.
parsedJson = json.loads(line)

# Get text from Reddit post.
if "comment" in parsedJson:
    textHtml = parsedJson["comment"]["body_html"]
    text = BeautifulSoup(textHtml, "lxml").text.strip()
else:
    text = parsedJson["submission"]["title"]

# Clean tweet text.
cleanedText = cleanTweetText(text, toLower=False, mustRemoveURLs=True)

# Get all interesting referred politicians in the tweet.
sentimentPolarity = getSentimentPolarity(cleanedText)

parsedJson["sentiment_polarity"] = str(sentimentPolarity)
enrichedJson = json.dumps(parsedJson)
print(enrichedJson)


