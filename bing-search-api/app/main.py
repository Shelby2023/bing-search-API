import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.schemas import SearchResponse
from app.providers.bing import BingV7Provider
from app.providers.serpapi_bing import SerpApiBingProvider

load_dotenv()

app = FastAPI(title="Bing 风格搜索 API 接口", version="1.0.0")

def choose_provider() -> str:
    # 优先选择仍可用的官方 Bing（如你的租户仍在白名单内）
    if os.getenv("BING_SEARCH_API_KEY"):
        return "bing-v7"
    elif os.getenv("SERPAPI_API_KEY"):
        return "serpapi-bing"
    else:
        return ""

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="搜索关键词"),
    count: int = Query(10, ge=1, le=50, description="返回结果条数"),
    mkt: str = Query("zh-CN", description="市场/语言，例如 zh-CN, en-US"),
    safe_search: str = Query("Moderate", description="Off | Moderate | Strict"),
    include_raw: bool = Query(False, description="是否返回底层原始响应（raw 字段）"),
    provider: str = Query(None, description="强制指定后端：bing-v7 或 serpapi-bing；缺省自动选择"),
):
    prov = provider or choose_provider()
    if prov == "bing-v7":
        try:
            data = await BingV7Provider.search(q, count=count, mkt=mkt, safe_search=safe_search, include_raw=include_raw)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"BingV7 调用失败: {e}")
    elif prov == "serpapi-bing":
        try:
            data = await SerpApiBingProvider.search(q, count=count, mkt=mkt, safe_search=safe_search, include_raw=include_raw)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"SerpAPI 调用失败: {e}")
    else:
        raise HTTPException(status_code=400, detail="未配置任何可用的后端提供方（需要 BING_SEARCH_API_KEY 或 SERPAPI_API_KEY）")

    return SearchResponse(query=q, **data)
