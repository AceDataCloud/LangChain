# ACE Music toolkit for LangChain

<img src="https://cdn.acedata.cloud/acemusic-icon-52deddfc87b9.png" width="64" height="64" alt="ACE Music" />

Look up a song group from an existing ACE Music task in a LangChain application. If your application should also submit new songs, enable the generation tool explicitly.

## Install and configure

```sh
python -m pip install langchain-acemusic-acedatacloud
```

Create an [application key with ACE Music access](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen) and load it into the `ACEDATACLOUD_API_TOKEN` environment variable. Keep the key outside prompts and source control.

## Retrieve a task

```python
import os

from langchain_acedatacloud import AceAPIClient
from langchain_acemusic_acedatacloud import AceMusicToolkit

toolkit = AceMusicToolkit(client=AceAPIClient())
(retrieve,) = toolkit.get_tools()
result = retrieve.invoke({"task_id": os.environ["ACE_MUSIC_TASK_ID"]})
print(result)
```

Use the original task ID for subsequent lookups. The result retains the raw task response, including partial track details. `get_tools()` exposes only `acemusic_retrieve_task` by default.

Set `AceMusicToolkit(client=AceAPIClient(), include_generation=True)` to add `acemusic_generate_audio`. Generation submits a paid operation. Choose `acemusic-v1.1` (default) or `acemusic-v1` and save the returned task ID before looking up the group. [API contract](https://github.com/AceDataCloud/ACEMusicAPI) · [Current pricing](https://platform.acedata.cloud/services/024e09b4-52cf-5e98-a91a-efedf43104c4?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen)

Set `include_assets=True` to enable free owned-asset reads. Setting `include_generation=True` as well enables paid reference import. Generate with both `asset_id` and `asset_type` using v1.1.
