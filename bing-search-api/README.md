# 🔎 Bing 搜索引擎 API 接口（Python/FastAPI 实现）

> **重要变更（2025）**：微软已宣布 **Bing Search APIs 将于 2025-08-11 正式退役**。大多数开发者将无法继续调用官方 Bing Web Search v7 接口，仅少数大客户可能保留访问。微软建议迁移到 *Azure AI Agents* 的 “Grounding with Bing Search”。本仓库提供两种接入方案：  
> A. （若你仍有白名单/存量权限）继续调用官方 **Bing Web Search v7**；  
> B. 使用 **SerpAPI** 的 `engine=bing` 作为替代，以保持接口能力与返回结构基本一致。

---

## 功能概述

- 提供 RESTful 接口 `GET /search?q=...`  
- 返回**结构化**的统一结果格式：`title / url / snippet / rank / source`
- 支持选择后端提供方：`bing-v7`（官方）或 `serpapi-bing`（替代）
- 附带 CLI 演示、最简单元测试、`.env` 示例

## 目录结构

```
bing-search-api/
├─ app/
│  ├─ main.py               # FastAPI 入口
│  ├─ schemas.py            # Pydantic 模型（统一返回结构）
│  └─ providers/
│     ├─ bing.py            # 官方 Bing v7 提供方
│     └─ serpapi_bing.py    # SerpAPI（engine=bing）替代
├─ cli.py                   # 命令行演示
├─ requirements.txt
├─ .env.example
├─ tests/
│  └─ test_smoke.py
└─ README.md
```

## 快速开始

### 1) 准备环境

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # 并填入密钥
```

### 2) 获取密钥

**方案 A（可能已不可用）**：Azure Bing Web Search v7  
- 创建/定位 “Bing Search v7” 资源（若你的订阅仍被允许）。  
- 记录 `Key` 与 `Endpoint`，填入 `.env`：

```
BING_SEARCH_API_KEY=你的Key
BING_SEARCH_ENDPOINT=https://api.bing.microsoft.com/v7.0/search
```

**方案 B（推荐）**：SerpAPI 的 Bing 引擎  
- 注册 SerpAPI，获取 `SERPAPI_API_KEY`：

```
SERPAPI_API_KEY=你的SerpAPIKey
```

> 说明：运行时若同时设置两者，默认优先使用官方 `bing-v7`；也可通过查询参数 `provider` 强制指定。

### 3) 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

访问：<http://127.0.0.1:8000/health> 与 <http://127.0.0.1:8000/docs>

### 4) 示例请求

**cURL**：
```bash
curl "http://127.0.0.1:8000/search?q=微软+Bing+API&count=5&mkt=zh-CN&safe_search=Moderate&include_raw=false"
```

**强制使用 SerpAPI**：
```bash
curl "http://127.0.0.1:8000/search?q=python+fastapi&provider=serpapi-bing&count=5"
```

**Python 客户端**：
```python
import requests

resp = requests.get("http://127.0.0.1:8000/search", params={"q": "FastAPI 教程", "count": 5})
print(resp.json())
```

**命令行（Typer）**：
```bash
python cli.py search "FastAPI" --provider serpapi-bing --count 3
```

## 统一返回结构

```json
{
  "query": "FastAPI",
  "provider": "serpapi-bing",
  "count": 3,
  "items": [
    {"title":"...","url":"https://...","snippet":"...","rank":1,"source":"serpapi-bing"},
    {"title":"...","url":"https://...","snippet":"...","rank":2,"source":"serpapi-bing"}
  ]
}
```

## 错误处理与限流建议

- 4xx：检查密钥/配额/可用性；Bing v7 可能返回 401/403/410（退役/权限问题）。
- 429：添加指数退避重试，控制 `count`，避免频繁请求。
- 网络超时：默认 20s，可在代码中调整 `httpx.AsyncClient(timeout=...)`。

## 测试

```bash
pytest -q
```

## 部署建议
- 部署到任意支持 Python 的平台（如 Render/自托管）。
- 可加上 WAF 与简单的 API Key 校验，避免被公共滥用。
- 若需要 Docker，自行添加 `Dockerfile`：
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 重要说明与参考

- **Bing Search APIs 退役时间：2025-08-11**（官方生命周期公告）。
- 微软迁移建议：使用 *Azure AI Agents* 的 **Grounding with Bing Search**（偏向 LLM 生成答案而非返回原始索引结果）。
- 若你无法继续使用官方 API，请启用 **SerpAPI**（`engine=bing`）或迁移到其它搜索 API（如 Brave/You.com 等）。

> 官方参考：
> - Bing Search APIs 退役公告（Microsoft Learn Lifecycle）  
>   https://learn.microsoft.com/en-us/lifecycle/announcements/bing-search-api-retirement
> - Web Search API v7 端点与头信息（若你的订阅仍可用）  
>   https://learn.microsoft.com/bing/search-apis/bing-web-search/reference/endpoints
> - 行业报道与替代方案讨论（The Verge / Wired / Windows Central / SERoundtable / SerpAPI 等）

---

### 常见问答

**Q：还能不能直接调用官方 Bing Web Search？**  
A：若你所在租户被白名单保留，仍可用；否则将收到 401/403/410 或资源被禁用。建议准备替代通道。

**Q：为什么 README 里提供两套实现？**  
A：为了最小化迁移成本，统一输出结构，便于用同一前端/调用方对接。

**Q：如何上传到 GitHub？**  
A：在本地解压本项目，执行：
```bash
git init
git add .
git commit -m "feat: 初版 Bing 风格搜索 API"
git branch -M main
git remote add origin <你的GitHub仓库URL>
git push -u origin main
```
