# GPT Image by Ace Data Cloud：LangChain中文接入

这个独立工具包把GPT Image的文本生成提交和同任务查询加入LangChain应用，由Ace Data Cloud提供，非服务品牌官方客户端。只安装本项服务及共用运行时，不带入其他四服务模块。[English](../README.md) · [发布状态](https://github.com/AceDataCloud/LangChain/blob/main/RELEASE_STATUS.md)。

## 1. 安装正确的候选包

源码已合入main，**0.1.0正式版**正在发布。执行下方安装命令前请查看[发布状态](../../../RELEASE_STATUS.md)，只有确实在PyPI存在的版本才可安装；官方目录是否收录另验。历史0.1.0rc1不冒充正式版。

Python 3.10或更新版本，先创建独立环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install langchain-gpt-image-acedatacloud==0.1.0
```

Windows PowerShell用 `.venv\Scripts\Activate.ps1` 激活；安装命令可以放在同一行执行。以上仅安装包，不提交模型或媒体请求。GitHub候选安装文件可在[release文件列表](https://github.com/AceDataCloud/LangChain/releases/tag/v0.1.0)核对。

## 2. 注册登录并获取应用Token

1. 打开[Ace应用页](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_gpt_image_zh_api_key)注册或登录。没有通用应用时先点 **Initialize General Application**。
2. 进入 **General application**。图中1复制现有API Key，图中2打开 **Manage Keys → Create**。建议专门命名为 `LangChain GPT Image`，方便撤销/轮换。
3. 检查有效期、用量限额和 **Allowed APIs**，同时允许 `/openai/images/generations` 与 `/openai/tasks`。确认GPT Image权限、余额和[当前模型／服务价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_gpt_image_zh_pricing)，不承诺固定试用金。

![真实控制台历史截图：复制Key或进入管理，凭据已遮挡](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![真实控制台历史截图：创建独立Key，图中Dify tutorial为历史名称](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

两图来源 [SunoDify固定commit](https://github.com/AceDataCloud/SunoDify/tree/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial)，2026-10-18复用核验；原截图日期／UI版本未标注。创建图中的 `Dify tutorial` 是历史示例名，实际填写 `LangChain GPT Image`。它们只说明Ace取Key，不冒充LangChain界面或本次调用。

只复制原始Token，不带 `Bearer `、引号、空格或截图遮挡字符。`platform-...` 是账户管理Token，不能替代生成应用Key。密钥不应出现在模型提示词、代码提交或共享工作流里。

## 3. 在本平台填写Key并确认工具

LangChain是Python框架，此包没有新的图形授权弹窗。填写位置是环境变量或应用的秘密管理器：

```bash
export ACEDATACLOUD_API_TOKEN='你的应用Token'
```

PowerShell：`$env:ACEDATACLOUD_API_TOKEN='你的应用Token'`。在代码中调用客户端，Key不进入模型的工具输入schema：

```python
from langchain_acedatacloud import AceAPIClient
from langchain_gpt_image_acedatacloud import GPTImageToolkit

kit = GPTImageToolkit(client=AceAPIClient())
print([tool.name for tool in kit.get_tools()])
# ['gpt_image_retrieve_task']
```

这一步只创建本地对象、展示工具名，不发网络请求。默认仅加载查询；把 `get_tools()` 交给LangChain Agent即可用原生BaseTool接口，实际Agent模型调用也可能收费。

## 4. 首次提交，再用相同ID查询结果

应用明确获准生成并确认当前价格后，启用生成工具。下面的 `generate.invoke` **会提交一次收费请求**；教程不自动执行：

```python
kit = GPTImageToolkit(client=AceAPIClient(), include_generation=True)
generate, retrieve = kit.get_tools()
submitted = generate.invoke({"prompt": "A minimal watercolor sunrise over a lake."})
task_id = submitted["task_id"]
result = retrieve.invoke({"task_id": task_id})
print(result["status"], result["terminal"], result["media_urls"])
```

`gpt_image_generate_image` 提交 `/openai/images/generations`，强制异步且不自动重试／后台轮询。`gpt_image_retrieve_task` 调用 `/openai/tasks`，只传 `action=retrieve` 和已有ID。

如果 `status=pending` 或 `terminal=false`，保留ID，稍后只查这一个ID；不要重新运行生成来等待。可在单独进程中查询历史任务：

```python
from langchain_acedatacloud import AceAPIClient
from langchain_gpt_image_acedatacloud import GPTImageToolkit

retrieve = GPTImageToolkit(client=AceAPIClient()).get_tools()[0]
result = retrieve.invoke({"task_id": "替换成你已经拥有的task_id"})
print(result["status"], result["terminal"], result["media_urls"])
```

终态只看工具返回的 `terminal` 及 `status`；失败终态不能当成功。预览媒体／提交成功不代表完成；最终媒体链接仅在结算完成后列出。返回格式为示例，不是本次真实生成截图。工具不自动下载媒体。初版只提供文本生成，不承诺全部edit、extend等高级动作。

## 5. 排错与实际计费

| 现象 | 检查 |
| --- | --- |
| 401／未配置Key | 原始应用Token、环境变量拼写；不要加Bearer。 |
| 403 | 服务权限、余额、有效期、额度、Allowed APIs和响应中的策略说明。 |
| 429 | 降低并发，等待后再决定；不要打开收费自动重试。 |
| pending／媒体为空 | 查同一ID；不要重新生成。 |
| 超时／5xx | 先查原任务和[使用历史](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langchain_gpt_image_zh_usage)，再决定是否重新提交。 |
| 媒体无法打开 | 核实任务成功终态、返回URL有效期和本机网络。 |

实际扣费以Credits使用历史为准；模型tokens、安装次数、候选下载不是营收。不要向维护者发送Key；排查提供task/trace ID即可。本指南的mock／候选安装验证不等于真实生成、终态媒体与唯一账单验收。
