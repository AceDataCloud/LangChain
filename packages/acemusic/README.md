# ACE Music toolkit for LangChain

From the repository root run `pip install ./packages/core ./packages/acemusic` and set the private `ACEDATACLOUD_API_TOKEN` environment variable to your [application key](https://platform.acedata.cloud/console/applications).

```python
from langchain_acedatacloud import AceAPIClient
from langchain_acemusic_acedatacloud import AceMusicToolkit

toolkit = AceMusicToolkit(client=AceAPIClient())
(retrieve,) = toolkit.get_tools()
# retrieve.invoke({"task_id": existing_task_id})
```

Set `include_generation=True` to add the paid idea-to-song tool. Choose `acemusic-v1.1` (default) or `acemusic-v1`, save the original task ID, and query that ID for the final group. The toolkit preserves the raw task for partial-track details. [API contract](https://github.com/AceDataCloud/ACEMusicAPI)
