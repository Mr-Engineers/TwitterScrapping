import http.client
import json

conn = http.client.HTTPSConnection("twitter-trends-by-location.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "e1b2351de2msh3926f8cbdbed91ep14586djsnd49839646a60",
    'x-rapidapi-host': "twitter-trends-by-location.p.rapidapi.com"
}

conn.request("GET", "/location/8706e50d618235f29e60fedbf1844cf3", headers=headers)

res = conn.getresponse()
data = res.read()

json_data = json.loads(data.decode("utf-8"))

if json_data.get("status") == "SUCCESS":
    trends = json_data.get("trending", {}).get("trends", [])
    poland_trends = [trend for trend in trends if trend.get("domain") == "Poland" or trend.get("domain") == "Only on X"]

    print(json.dumps(poland_trends, indent=2, ensure_ascii=False))
else:
    print("Błąd w odpowiedzi:", json_data.get("message"))