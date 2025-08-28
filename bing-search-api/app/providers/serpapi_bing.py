import os
import httpx
from typing import Dict

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

class SerpApiBingProvider:
    name = "serpapi-bing"
    endpoint = "https://serpapi.com/search.json"

    @staticmethod
    async def search(query: str, *, count: int = 10, mkt: str = "zh-CN", safe_search: str = "Moderate", include_raw: bool = False) -> Dict:
        if not SERPAPI_KEY:
            raise RuntimeError("缺少环境变量 SERPAPI_API_KEY")

        params = {
            "engine": "bing",
            "q": query,
            "hl": mkt,
            "safe": "on" if safe_search.lower() != "off" else "off",
            "api_key": SERPAPI_KEY,
            "num": count,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.get(SerpApiBingProvider.endpoint, params=params)
            r.raise_for_status()
            data = r.json()

        # SerpAPI Bing 引擎返回字段解析
        organic = data.get("organic_results", []) or []
        items = []
        for i, it in enumerate(organic[:count], start=1):
            items.append({
                "title": it.get("title",""),
                "url": it.get("link",""),
                "snippet": it.get("snippet","") or "",
                "rank": i,
                "source": SerpApiBingProvider.name,
            })
        return {
            "provider": SerpApiBingProvider.name,
            "count": len(items),
            "items": items,
            "raw": data if include_raw else None,
        }
