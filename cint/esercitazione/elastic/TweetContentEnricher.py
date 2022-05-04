import fileinput
import json

import string
import re

stopwords = {
    "en":set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]),
    "it": set(['ad', 'al', 'allo', 'ai', 'agli', 'all', 'agl', 'alla', 'alle', 'con', 'col', 'coi', 'da', 'dal', 'dallo', 'dai', 'dagli', 'dall', 'dagl', 'dalla', 'dalle', 'di', 'del', 'dello', 'dei', 'degli', 'dell', 'degl', 'della', 'delle', 'in', 'nel', 'nello', 'nei', 'negli', 'nell', 'negl', 'nella', 'nelle', 'su', 'sul', 'sullo', 'sui', 'sugli', 'sull', 'sugl', 'sulla', 'sulle', 'per', 'tra', 'contro', 'io', 'tu', 'lui', 'lei', 'noi', 'voi', 'loro', 'mio', 'mia', 'miei', 'mie', 'tuo', 'tua', 'tuoi', 'tue', 'suo', 'sua', 'suoi', 'sue', 'nostro', 'nostra', 'nostri', 'nostre', 'vostro', 'vostra', 'vostri', 'vostre', 'mi', 'ti', 'ci', 'vi', 'lo', 'la', 'li', 'le', 'gli', 'ne', 'il', 'un', 'uno', 'una', 'ma', 'ed', 'se', 'perché', 'anche', 'come', 'dov', 'dove', 'che', 'chi', 'cui', 'non', 'più', 'quale', 'quanto', 'quanti', 'quanta', 'quante', 'quello', 'quelli', 'quella', 'quelle', 'questo', 'questi', 'questa', 'queste', 'si', 'tutto', 'tutti', 'a', 'c', 'e', 'i', 'l', 'o', 'ho', 'hai', 'ha', 'abbiamo', 'avete', 'hanno', 'abbia', 'abbiate', 'abbiano', 'avrò', 'avrai', 'avrà', 'avremo', 'avrete', 'avranno', 'avrei', 'avresti', 'avrebbe', 'avremmo', 'avreste', 'avrebbero', 'avevo', 'avevi', 'aveva', 'avevamo', 'avevate', 'avevano', 'ebbi', 'avesti', 'ebbe', 'avemmo', 'aveste', 'ebbero', 'avessi', 'avesse', 'avessimo', 'avessero', 'avendo', 'avuto', 'avuta', 'avuti', 'avute', 'sono', 'sei', 'è', 'siamo', 'siete', 'sia', 'siate', 'siano', 'sarò', 'sarai', 'sarà', 'saremo', 'sarete', 'saranno', 'sarei', 'saresti', 'sarebbe', 'saremmo', 'sareste', 'sarebbero', 'ero', 'eri', 'era', 'eravamo', 'eravate', 'erano', 'fui', 'fosti', 'fu', 'fummo', 'foste', 'furono', 'fossi', 'fosse', 'fossimo', 'fossero', 'essendo', 'faccio', 'fai', 'facciamo', 'fanno', 'faccia', 'facciate', 'facciano', 'farò', 'farai', 'farà', 'faremo', 'farete', 'faranno', 'farei', 'faresti', 'farebbe', 'faremmo', 'fareste', 'farebbero', 'facevo', 'facevi', 'faceva', 'facevamo', 'facevate', 'facevano', 'feci', 'facesti', 'fece', 'facemmo', 'faceste', 'fecero', 'facessi', 'facesse', 'facessimo', 'facessero', 'facendo', 'sto', 'stai', 'sta', 'stiamo', 'stanno', 'stia', 'stiate', 'stiano', 'starò', 'starai', 'starà', 'staremo', 'starete', 'staranno', 'starei', 'staresti', 'starebbe', 'staremmo', 'stareste', 'starebbero', 'stavo', 'stavi', 'stava', 'stavamo', 'stavate', 'stavano', 'stetti', 'stesti', 'stette', 'stemmo', 'steste', 'stettero', 'stessi', 'stesse', 'stessimo', 'stessero', 'stando'])
}

# Remove any URL from text.
def removeURLs(text):
    cleanText = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    return cleanText

# Remove all special chars from text.
def removeSpecialChars(text):
    cleanText = re.sub(r'[\r\n]+', ' ', text, flags=re.MULTILINE)
    cleanText = cleanText.replace("RT", "")
    return cleanText


def removeAllPuntuaction(text):
    ret = ""
    for c in text:
        if c in string.punctuation:
            ret = ret + " "
        else:
            ret = ret + c
    tokens = re.compile(r"\s+").split(ret.strip())
    return " ".join(tokens)

# Get a clean tweet text.
def cleanTweetText(text, lang, toLower= False, mustRemoveURLs=False):
   

    if toLower:
        textRet = text.lower()
    else:
        textRet = text
    if mustRemoveURLs:
        textRet = removeURLs(textRet)
    textRet = removeSpecialChars(textRet)

    textRet = removeAllPuntuaction(textRet)

    tokens = re.compile(r"\s+").split(textRet)

    if lang in stopwords:
        swords = stopwords[lang]
        filtered_words = [w for w in tokens if w if not w in swords]
        return " ".join(filtered_words).strip()
    else:
        return " ".join(tokens).strip()



def enrichContent(parsedJson):
    if "retweeted_status" in parsedJson:
        return None    

    # Get tweet text.
    text = parsedJson["text"]

    # Get tweet language.
    tweetLanguage = parsedJson["lang"]

    imageFound = ""
    videoFound = ""
    if ("extended_entities" in parsedJson) and ("media" in parsedJson["extended_entities"]):
        medias = parsedJson["extended_entities"]["media"]
        for m in medias:
            if m["type"] == "photo":
                imageFound = m["expanded_url"]
            if m["type"] == "video":
                videoFound = m["expanded_url"]

    cleanText = cleanTweetText(text, tweetLanguage, toLower=True, mustRemoveURLs=True)
    

    return {"cleanText":cleanText,
            "imageUrl":imageFound,
            "videoUrl":videoFound}






# Read data coming from stdin
line = input()

# Parse JSON data.
parsedJson = json.loads(line)

# Clean tweet text.
enrichedData = enrichContent(parsedJson)
if enrichedData is None:
    parsedJson["enrichedData"] = {}
else:
    parsedJson["enrichedData"] = enrichedData
enrichedJson = json.dumps(parsedJson)
print(enrichedJson)


