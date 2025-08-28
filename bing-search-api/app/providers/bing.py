import os
import httpx
from typing import List, Dict

BING_ENDPOINT = os.getenv("BING_SEARCH_ENDPOINT", "http://bing.ydcloud.org:4399/api/v1/v7.0/search")
BING_KEY = os.getenv("BING_SEARCH_API_KEY")

class BingV7Provider:
    name = "bing-v7"

    @staticmethod
    async def search(query: str, *, count: int = 10, mkt: str = "zh-CN", safe_search: str = "Moderate", include_raw: bool = False) -> Dict:
        if not BING_KEY:
            raise RuntimeError("缺少环境变量 BING_SEARCH_API_KEY")

        headers = {
            "Ocp-Apim-Subscription-Key": BING_KEY,
        }
        params = {
            "q": query,
            "count": count,
            "mkt": mkt,
            "safeSearch": safe_search,
            # 也可使用 "responseFilter": "Webpages"
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.get(BING_ENDPOINT, headers=headers, params=params)
            # 如果 API 已退役或不可用，可能返回 401/403/404/410
            r.raise_for_status()
            data = r.json()
        # 解析结构
        items = []
        rank = 1
        for wp in (data.get("webPages", {}) or {}).get("value", []):
            items.append({
                "title": wp.get("name",""),
                "url": wp.get("url",""),
                "snippet": wp.get("snippet","") or wp.get("about","") or "",
                "rank": rank,
                "source": BingV7Provider.name,
            })
            rank += 1
        return {
            "provider": BingV7Provider.name,
            "count": len(items),
            "items": items,
            "raw": data if include_raw else None,
        }
