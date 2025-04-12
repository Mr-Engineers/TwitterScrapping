import http.client
import json
from pymongo import MongoClient
from datetime import datetime

conn = http.client.HTTPSConnection("twitter-trends-by-location.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "e1b2351de2msh3926f8cbdbed91ep14586djsnd49839646a60",
    'x-rapidapi-host': "twitter-trends-by-location.p.rapidapi.com"
}

conn.request("GET", "/location/8706e50d618235f29e60fedbf1844cf3", headers=headers)

res = conn.getresponse()
data = res.read()

json_data = json.loads(data.decode("utf-8"))
poland_trends = None

if json_data.get("status") == "SUCCESS":
    trends = json_data.get("trending", {}).get("trends", [])
    poland_trends = [trend for trend in trends if trend.get("domain") == "Poland" or trend.get("domain") == "Only on X"]

    print(json.dumps(poland_trends, indent=2, ensure_ascii=False))
else:
    print("Błąd w odpowiedzi:", json_data.get("message"))

uri = "mongodb+srv://root:root@hacknarok.quwkjxf.mongodb.net/?retryWrites=true&w=majority&appName=Hacknarok"
client = MongoClient(uri)
db = client["Hacknarok"]
collection = db["Twitter"]

if poland_trends:
    for trend in poland_trends:
        collection.insert_one({
            "name": trend.get("name"),
            "post_count": trend.get("postCount"),
            "rank": trend.get("rank"),
            "date": datetime.now().strftime("%Y-%m-%d")
        })
