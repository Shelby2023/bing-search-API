import os
import pytest
import asyncio
from app.providers.serpapi_bing import SerpApiBingProvider

@pytest.mark.asyncio
async def test_serpapi_env_missing():
    # 临时清空环境变量以验证错误
    old = os.environ.pop("SERPAPI_API_KEY", None)
    try:
        with pytest.raises(RuntimeError):
            await SerpApiBingProvider.search("test")
    finally:
        if old:
            os.environ["SERPAPI_API_KEY"] = old
