# Based on example available at https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Filtered-Stream/filtered_stream.py
#
# A Twitter client listening on real-time streaming data.
# To use the software you must specify:
# 1) Your bearer token as available in Twitter developer dashboard of your project: https://developer.twitter.com/en/portal/dashboard
# 2) A query rule defined with the standard operatore ddescribed in https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule#availability
# 
# In the following we show some possible query rules you can use to search for tweets:
# -----   "(conte OR salvini OR meloni OR letta) -is:retweet -is:reply -is:quote lang:it"
#         to search for tweets including one of the specified keywords and not including tweets that are retweets, replies 
#         or quotes of other tweets
# -----   "#nowar 😡" for every type of tweet (original, replies, etc.) mentioning the hashtag nowar and with the angry emoji.




import requests
import os
import json
import argparse




def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )


def set_rules(rules):
    
    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    #print(json.dumps(response.json()))


def extractHashtags(jsonData):
    ent = jsonData["data"]["entities"]
    if not "hashtags" in ent:
        return []
    hashtags = ent["hashtags"]
    ret = []
    for h in hashtags:
        ret.append(h["tag"])
    return ret

def extractMentions(jsonData):
    ent = jsonData["data"]["entities"]
    if not "mentions" in ent:
        return []
    mentions = ent["mentions"]
    ret = []
    for m in mentions:
        ret.append(m["username"])
    return ret

def extractUrls(jsonData):
    ent = jsonData["data"]["entities"]
    if not "urls" in ent:
        return []
    urls = ent["urls"]
    ret = []
    for u in urls:
        ret.append(u["expanded_url"])
    return ret


def extractCtxAnnotations(jsonData):
    if not "context_annotations" in jsonData["data"]:
        return []
    ctx = jsonData["data"]["context_annotations"]
    ret = []
    for ann in ctx:
        annotation = {}
        annotation["type"] = ann["domain"]["name"]
        annotation["name"] = ann["entity"]["name"]
        if "description" in ann["entity"]:
            annotation["description"] = ann["entity"]["description"]
        else:
            annotation["description"] = ""
        ret.append(annotation)
    return ret

def getUserData(jsonData, userID):
    users = jsonData["includes"]["users"]
    for u in users:
        if u["id"] == userID:
            return u
    print("Error: no user found for ID: "+userID+"!")
    return None

def simplifyDataFormat(jsonData):
    data = {}

    # Extract tweet data
    tweet = {}
    tweet["id"] = jsonData["data"]["id"]
    tweet["created_at"] = jsonData["data"]["created_at"]
    tweet["text"] = jsonData["data"]["text"]
    tweet["lang"] = jsonData["data"]["lang"]
    tweet["retweet_count"] = jsonData["data"]["public_metrics"]["retweet_count"]
    tweet["reply_count"] = jsonData["data"]["public_metrics"]["reply_count"]
    tweet["like_count"] = jsonData["data"]["public_metrics"]["like_count"]
    tweet["quote_count"] = jsonData["data"]["public_metrics"]["quote_count"]
    tweet["geo"] = jsonData["data"]["geo"]
    tweet["hashtags"] = extractHashtags(jsonData)
    tweet["mentions"] = extractMentions(jsonData)
    tweet["urls"] = extractUrls(jsonData)
    tweet["ctx_annotations"] = extractCtxAnnotations(jsonData)

    # Extract user data
    userID = jsonData["data"]["author_id"]
    userData = getUserData(jsonData, userID)
    user = {}
    user["created_at"] = userData["created_at"]
    user["description"] = userData["description"]
    user["id"] = userData["id"]
    user["name"] = userData["name"]
    user["profile_image_url"] = userData["profile_image_url"]
    user["followers_count"] = userData["public_metrics"]["followers_count"]
    user["following_count"] = userData["public_metrics"]["following_count"]
    user["tweet_count"] = userData["public_metrics"]["tweet_count"]
    user["listed_count"] = userData["public_metrics"]["listed_count"]
    user["url"] = userData["url"]
    user["username"] = userData["username"]
    user["verified"] = userData["verified"]

    data["tweet"] = tweet
    data["user"] = user

    return data




def get_stream():
    req = "https://api.twitter.com/2/tweets/search/stream?tweet.fields=" # For tweet info
    req += "created_at"
    req += ",context_annotations"
    req += ",entities"
    req += ",geo"
    req += ",lang"
    req += ",public_metrics"
    req += "&expansions=author_id&user.fields=" # For user info
    req += "created_at"
    req += ",name"
    req += ",username"
    req += ",description"
    req += ",location"
    req += ",profile_image_url"
    req += ",public_metrics"
    req += ",url"
    req += ",verified"



    response = requests.get(
        req, auth=bearer_oauth, stream=True,
    )
    
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            simplifiedJson = simplifyDataFormat(json_response)
            #print("<SEP>")
            print(json.dumps(simplifiedJson))
            



def main():

    import argparse

    parser = argparse.ArgumentParser(description="Twitter stream listener using Twitter API 2.0",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("bearer_token", help="Bearer token to use while calling Twitter APIs")
    parser.add_argument("twitter_query_rule", help="The rule using Twitter operators to query Twitter for data. See https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule#availability for some example.")
    args = parser.parse_args()
    config = vars(args)
    
    global bearer_token 
    bearer_token = config["bearer_token"]
    twitter_query_rule = config["twitter_query_rule"]
    rules = [
        {"value": twitter_query_rule, "tag": "query rule"},
    ]


    old_rules = get_rules()
    delete_all_rules(old_rules)
    set = set_rules(rules)
    get_stream()


if __name__ == "__main__":
    main()