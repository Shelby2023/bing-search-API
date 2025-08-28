import requests

resp = requests.get("http://127.0.0.1:8000/search", params={"q": "杭州美食", "count": 5})
print(resp.json())