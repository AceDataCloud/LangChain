# Google Search toolkit for LangChain

<img src="https://cdn.acedata.cloud/27e11e555d.png" width="64" height="64" alt="Google Search via Ace Data Cloud" />

Give a LangChain agent a web search tool that returns Google's organic results, including the title, source link, and snippet when available. It uses the Ace Data Cloud Serp API and accepts optional country, language, result count, and page parameters.

```sh
python -m pip install langchain-serp-acedatacloud
```

Set `ACEDATACLOUD_API_TOKEN` to an [application key with Serp access](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen). Creating the toolkit and listing its tools makes no request. Each invocation performs one billable search for the selected page.

```python
from langchain_serp_acedatacloud import SerpToolkit

(search,) = SerpToolkit().get_tools()
response = search.invoke({"query": "LangChain tool calling documentation", "number": 5})
for result in response.get("organic", []):
    print(result.get("title"), result.get("link"), result.get("snippet"))
```

Use `await search.ainvoke({...})` for async applications. The response preserves the provider's result fields and reported cost. To retrieve a later page, send an explicit `page` value. Avoid automatically retrying an ambiguous request because each new search can consume credits. [OpenAPI contract](https://docs.acedata.cloud/openapi/serp.json)
