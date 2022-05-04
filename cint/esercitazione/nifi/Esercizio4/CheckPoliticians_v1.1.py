import fileinput
import json

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


def getAllReferredPoliticians(text, politiciansName):
    # Prepare tweet text to be analyzed with polyglot.
    textForAnalysis = Text(text, hint_language_code="it")
    tweetPolarity = 0
    for w in textForAnalysis.words:
        tweetPolarity = tweetPolarity + w.polarity

    # Extract all entities of type "person", including info about positive
    # or negative sentiment about that specific person.
    peopleTagged = []
    entities = textForAnalysis.entities
    for entity in entities:
        if entity.tag == "I-PER":
            person = " ".join(entity)
            if person in politiciansName:
                peopleTagged.append(politiciansName.get(person))

    return {"polarity":str(tweetPolarity), "names":peopleTagged}



politiciansTweetID = {"@matteorenzi": "Renzi",
               "@matteosalvinimi":"Salvini",
               "@luigidimaio": "Di Maio",
               "@berlusconi":"Berlusconi",
		"@GiuseppeConteIT":"Conte"}

politiciansName = {"Renzi":"Renzi",
                       "Matteo Renzi":"Renzi",
                       "Salvini":"Salvini",
                       "Matteo Salvini":"Salvini",
                       "Di Maio":"Di Maio",
                       "Luigi Di Maio": "Di Maio",
                       "Berlusconi": "Berlusconi",
                       "Silvio Berlusconi": "Berlusconi",
			"Giuseppe Conte": "Conte",
			"Conte": "Conte"
}


# Read data coming from stdin. 
line = input()

# Parse JSON data.
parsedJson = json.loads(line)

# Get tweet text.
text = parsedJson["text"]

# Replace all politicians Twitter IDs with their corresponding name.
for key,value in politiciansTweetID.items():
    text = text.replace(key, value)

# Clean tweet text.
cleanedText = cleanTweetText(text, toLower=False, mustRemoveURLs=True)

# Get all interesting referred politicians in the tweet.
allPoliticians = getAllReferredPoliticians(cleanedText, politiciansName)

parsedJson["politicians"] = allPoliticians
enrichedJson = json.dumps(parsedJson)
print(enrichedJson)


