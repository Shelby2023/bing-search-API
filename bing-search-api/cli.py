import os, sys
sys.path.insert(0, os.path.dirname(__file__))  # 项目根优先

import asyncio
import json
import typer
from app.providers.bing import BingV7Provider
from app.providers.serpapi_bing import SerpApiBingProvider

app = typer.Typer(help="命令行搜索演示")

@app.command()
def search(query: str, provider: str = typer.Option("bing-v7", help="bing-v7 或 serpapi-bing"), count: int = 5):
    async def _run():
        if provider == "bing-v7":
            data = await BingV7Provider.search(query, count=count, include_raw=False)
        else:
            data = await SerpApiBingProvider.search(query, count=count, include_raw=False)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    asyncio.run(_run())

if __name__ == "__main__":
    app()
