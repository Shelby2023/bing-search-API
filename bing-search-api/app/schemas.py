from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Literal

class SearchResultItem(BaseModel):
    title: str = Field(..., description="结果标题")
    url: HttpUrl = Field(..., description="结果URL")
    snippet: str = Field("", description="摘要/描述")
    rank: int = Field(..., description="结果排序序号（从1开始）")
    source: Literal["bing-v7","serpapi-bing"] = Field(..., description="提供该结果的后端源")

class SearchResponse(BaseModel):
    query: str
    provider: Literal["bing-v7","serpapi-bing"]
    count: int
    items: List[SearchResultItem]
    raw: Optional[dict] = None
