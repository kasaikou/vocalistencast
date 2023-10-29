import requests
import pandas as pd
import os
import json

DATABASE_SECRET=os.getenv("NOTIONAPI_SECRET")
if DATABASE_SECRET is None:
    raise RuntimeError("NOTIONAPI_SECRET is None")

DATABASE_ID=os.getenv("NOTIONAPI_DBID")
if DATABASE_ID is None:
    raise RuntimeError("NOTIONAPI_DBID is None")

notion_dbcolumns = {
    "NicoUrl": "ニコニコ",
    "NicoId": "ニコニコID",
    "Title": "名前",
    "IsPlayed": "曲を聴いた",
    "SelfTweetUrl": "自薦ツイートリンクorID",
    "RequestTweetUrl": "他薦ツイートリンクorID",
}

def read_database() -> pd.DataFrame:
    df = pd.DataFrame()

    while True:
        body = {}
        
        res = requests.post(
            f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
            headers={
                "Authorization": f"Bearer {DATABASE_SECRET}",
                "Notion-Version": "2022-06-28",
            },
            json=body,
        )

        content = json.loads(res.content)
        results = content["results"]

        df = pd.concat([df, pd.DataFrame({
            "NicoUrl": [result["properties"][notion_dbcolumns["NicoUrl"]]["url"] for result in results],
            "NicoId": [result["properties"][notion_dbcolumns["NicoId"]]["formula"]["string"] for result in results],
            "Title": [result["properties"][notion_dbcolumns["Title"]]["title"][0]["plain_text"] for result in results],
            "IsPlayed": [result["properties"][notion_dbcolumns["IsPlayed"]]["checkbox"] for result in results],
        })])

        if content["has_more"] == False or content["next_cursor"] is None:
            return df
        body["start_cursor"] = content["next_cursor"]
