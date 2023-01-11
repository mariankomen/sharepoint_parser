from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests
import browsercookie
from urllib.parse import urlparse, parse_qs, urlunparse, urlunsplit, quote

app = FastAPI()

class Item(BaseModel):
    link: str

@app.post("/")
async def root(items: List[Item]):
    response = []

    for item in items:
        cj = browsercookie.load()
        r = requests.get(item.link, cookies=cj)

        o = urlparse(r.url)
        query = parse_qs(o.query)
        new_link = urlunsplit((o.scheme, o.netloc, quote(query['id'][0]), '', ""))

        response.append({
            "input_link": item.link,
            "cookies": r.cookies,
            "new_link": new_link
        })
    return response